/**
 * ChatKit initialization and dynamic interaction script
 */

(function initializeChatKit() {
  const CONFIG = {
    workflowId: document.currentScript?.dataset.workflowId || '',
    sessionEndpoint: document.currentScript?.dataset.sessionEndpoint || '/api/create-session',
    placeholder: document.currentScript?.dataset.placeholder || 'Ask anything...',
    greeting: document.currentScript?.dataset.greeting || 'How can I help you today?',
  };

  const chatkitContainer = document.getElementById('chatkit-container');
  const errorOverlay = document.getElementById('error-overlay');
  const errorMessage = document.getElementById('error-message');
  const retryButton = document.getElementById('retry-button');
  const themeToggle = document.getElementById('theme-toggle');

  let chatkitElement = null;

  function showError(message, retryable = true) {
    console.error('[ChatKit]', message);
    if (errorMessage) {
      errorMessage.textContent = message;
    }
    if (errorOverlay) {
      errorOverlay.style.display = 'flex';
    }
    if (retryButton && !retryable) {
      retryButton.style.display = 'none';
    }
  }

  function hideError() {
    if (errorOverlay) {
      errorOverlay.style.display = 'none';
    }
  }

  function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateChatkitTheme();
  }

  function initializeTheme() {
    const saved = localStorage.getItem('theme');
    const prefer = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = saved ? saved === 'dark' : prefer;
    
    if (isDark) {
      document.documentElement.classList.add('dark');
    }
    
    if (themeToggle) {
      themeToggle.addEventListener('click', toggleTheme);
    }
  }

  function updateChatkitTheme() {
    if (chatkitElement) {
      const isDark = document.documentElement.classList.contains('dark');
      chatkitElement.theme = isDark ? 'dark' : 'light';
    }
  }

  async function createSession() {
    try {
      const response = await fetch(CONFIG.sessionEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          workflow: { id: CONFIG.workflowId },
          chatkit_configuration: {
            file_upload: { enabled: false },
          },
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create session');
      }

      return await response.json();
    } catch (error) {
      console.error('[ChatKit] Session creation error:', error);
      throw error;
    }
  }

  async function initChatKit() {
    try {
      // Check if ChatKit is available
      if (!customElements.get('openai-chatkit')) {
        showError('ChatKit component not loaded. Please refresh the page.');
        return;
      }

      hideError();

      // Create session
      const session = await createSession();
      
      // Create ChatKit element
      chatkitElement = document.createElement('openai-chatkit');
      chatkitElement.sessionToken = session.token;
      chatkitElement.placeholder = CONFIG.placeholder;
      chatkitElement.greetingText = CONFIG.greeting;
      
      updateChatkitTheme();

      if (chatkitContainer) {
        chatkitContainer.innerHTML = '';
        chatkitContainer.appendChild(chatkitElement);
      }
    } catch (error) {
      showError(`Failed to initialize ChatKit: ${error.message}`);
      if (retryButton) {
        retryButton.onclick = initChatKit;
      }
    }
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initializeTheme();
      initChatKit();
    });
  } else {
    initializeTheme();
    initChatKit();
  }

  // Expose retry function
  window.retryChatKit = initChatKit;
})();
