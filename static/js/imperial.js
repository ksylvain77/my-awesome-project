/**
 * Imperial Threat Generator JavaScript
 * Handles interactive threat display and API communication
 */

// Imperial sound effects (using Web Audio API for breathing)
class ImperialSounds {
  constructor() {
    this.audioContext = null;
    this.init();
  }

  init() {
    try {
      this.audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
    } catch (e) {
      console.log('Web Audio API not supported');
    }
  }

  playBreathing() {
    if (!this.audioContext) return;

    // Create a simple breathing sound effect
    const oscillator = this.audioContext.createOscillator();
    const gainNode = this.audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.audioContext.destination);

    oscillator.type = 'sawtooth';
    oscillator.frequency.setValueAtTime(60, this.audioContext.currentTime);

    gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(
      0.1,
      this.audioContext.currentTime + 0.1
    );
    gainNode.gain.linearRampToValueAtTime(
      0,
      this.audioContext.currentTime + 0.8
    );

    oscillator.start(this.audioContext.currentTime);
    oscillator.stop(this.audioContext.currentTime + 0.8);
  }
}

// Main Imperial Threat Generator Class
class ImperialThreatGenerator {
  constructor() {
    this.apiBaseUrl = window.location.origin;
    this.sounds = new ImperialSounds();
    this.isLoading = false;
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.startBreathingEffect();
    this.updateThreatStats();
  }

  setupEventListeners() {
    // New threat button
    const newThreatBtn = document.getElementById('newThreatBtn');
    if (newThreatBtn) {
      newThreatBtn.addEventListener('click', () => this.getNewThreat());
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.code === 'Space' || e.code === 'Enter') {
        e.preventDefault();
        this.getNewThreat();
      }
    });

    // Breathing effect on helmet click
    const helmet = document.querySelector('.vader-helmet');
    if (helmet) {
      helmet.addEventListener('click', () => {
        this.sounds.playBreathing();
        this.addBreathingPulse();
      });
    }
  }

  async getNewThreat() {
    if (this.isLoading) return;

    this.isLoading = true;
    this.showLoadingState();

    try {
      const response = await fetch(`${this.apiBaseUrl}/api/threat`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const threatData = await response.json();
      this.displayNewThreat(threatData.threat);
      this.addThreatAnimation();
    } catch (error) {
      console.error('Failed to fetch new threat:', error);
      this.showError('The Force is weak with this connection...');
    } finally {
      this.isLoading = false;
      this.hideLoadingState();
    }
  }

  displayNewThreat(threat) {
    const threatText = document.getElementById('threatText');
    if (!threatText) return;

    // Fade out current threat
    threatText.style.transition = 'opacity 0.3s ease';
    threatText.style.opacity = '0';

    setTimeout(() => {
      threatText.textContent = threat;
      threatText.style.opacity = '1';
    }, 300);
  }

  addThreatAnimation() {
    const threatFrame = document.querySelector('.threat-frame');
    if (!threatFrame) return;

    threatFrame.classList.add('threat-pulse');
    setTimeout(() => {
      threatFrame.classList.remove('threat-pulse');
    }, 1000);
  }

  addBreathingPulse() {
    const helmet = document.querySelector('.vader-helmet');
    if (!helmet) return;

    helmet.classList.add('breathing-pulse');
    setTimeout(() => {
      helmet.classList.remove('breathing-pulse');
    }, 2000);
  }

  showLoadingState() {
    const button = document.getElementById('newThreatBtn');
    if (!button) return;

    button.disabled = true;
    button.innerHTML =
      '<span class="button-glow"></span>CHANNELING THE DARK SIDE...';
    button.classList.add('loading');
  }

  hideLoadingState() {
    const button = document.getElementById('newThreatBtn');
    if (!button) return;

    button.disabled = false;
    button.innerHTML = '<span class="button-glow"></span>GENERATE NEW THREAT';
    button.classList.remove('loading');
  }

  showError(message) {
    const threatText = document.getElementById('threatText');
    if (!threatText) return;

    const originalText = threatText.textContent;
    threatText.textContent = message;
    threatText.style.color = '#ff6666';

    setTimeout(() => {
      threatText.textContent = originalText;
      threatText.style.color = '';
    }, 3000);
  }

  async updateThreatStats() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/threat/count`);
      if (response.ok) {
        const data = await response.json();
        const countElement = document.getElementById('threatCount');
        if (countElement) {
          countElement.textContent = data.total_threats;
        }
      }
    } catch (error) {
      console.error('Failed to update threat stats:', error);
    }
  }

  startBreathingEffect() {
    // Add subtle breathing animation to various elements
    setInterval(() => {
      this.addSubtleBreathing();
    }, 4000);
  }

  addSubtleBreathing() {
    const elements = document.querySelectorAll(
      '.breathing-indicator, .death-star'
    );
    elements.forEach((element) => {
      element.style.animation = 'none';
      element.offsetHeight; // Trigger reflow
      element.style.animation = null;
    });
  }
}

// Additional CSS animations for JavaScript interactions
const additionalStyles = `
    .threat-pulse {
        animation: threatPulseEffect 1s ease-in-out !important;
    }
    
    @keyframes threatPulseEffect {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); box-shadow: 0 0 50px rgba(255, 0, 0, 0.5); }
        100% { transform: scale(1); }
    }
    
    .breathing-pulse {
        animation: breathingPulseEffect 2s ease-in-out !important;
    }
    
    @keyframes breathingPulseEffect {
        0% { transform: scale(1); }
        25% { transform: scale(1.1); }
        50% { transform: scale(1.05); }
        75% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .imperial-button.loading {
        background: linear-gradient(45deg, #660000 0%, #330000 50%, #660000 100%);
        animation: loadingPulse 1s ease-in-out infinite alternate;
    }
    
    @keyframes loadingPulse {
        0% { opacity: 0.7; }
        100% { opacity: 1; box-shadow: 0 0 30px #ff0000; }
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Initialize the Imperial Threat Generator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.imperialThreatGenerator = new ImperialThreatGenerator();

  // Add keyboard shortcut hint
  console.log('🌟 Imperial Tip: Press SPACE or ENTER to generate new threats!');
  console.log("🌟 Click on Vader's helmet for breathing effects!");
});

// Export for potential external use
window.ImperialThreatGenerator = ImperialThreatGenerator;
