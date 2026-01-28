let audioContext;
let recorder;
let audioInput;
let isRecording = false;
let isSpeaking = false;
let currentAudio = null;

// DOM Elements
const chatMessages = $("#chatMessages");
const messageInput = $("#messageInput");
const messageForm = $("#messageForm");
const micButton = $("#micButton");
const sendButton = $("#sendButton");
const themeToggle = $("#themeToggle");
const voiceSelect = $("#voiceSelect");
const recordingIndicator = $("#recordingIndicator");
const loadingOverlay = $("#loadingOverlay");

// Initialize on document ready
$(document).ready(function () {
  console.log("Voice Assistant initialized");

  // Load theme preference
  loadTheme();

  // Event listeners
  messageForm.on("submit", handleSendMessage);
  micButton.on("click", handleMicrophone);
  themeToggle.on("click", toggleTheme);
});

/**
 * Handle sending text messages
 */
function handleSendMessage(e) {
  e.preventDefault();

  const message = messageInput.val().trim();

  if (message === "") {
    return;
  }

  // Display user message
  displayMessage(message, "user");

  // Clear input
  messageInput.val("");

  // Process message
  processMessage(message);
}

/**
 * Handle microphone button click
 */
async function handleMicrophone() {
  if (isSpeaking) {
    stopAudioPlayback();
    return;
  }

  if (!isRecording) {
    await startRecording();
  } else {
    await stopRecording();
  }
}

/**
 * Start recording audio
 */
async function startRecording() {
  try {
    // Request microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Initialize AudioContext
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    audioInput = audioContext.createMediaStreamSource(stream);

    // Create recorder node
    // Buffer size 4096, 1 input channel, 1 output channel
    recorder = audioContext.createScriptProcessor(4096, 1, 1);

    let leftchannel = [];
    let recordingLength = 0;

    recorder.onaudioprocess = function (e) {
      if (!isRecording) return;
      const left = e.inputBuffer.getChannelData(0);
      // Clone samples
      leftchannel.push(new Float32Array(left));
      recordingLength += left.length;
    };

    // Connect nodes
    audioInput.connect(recorder);
    recorder.connect(audioContext.destination);

    // Store reference to buffer for stopRecording
    recorder.leftchannel = leftchannel;
    recorder.recordingLength = recordingLength;

    isRecording = true;

    // Update UI
    micButton.addClass("recording");
    micButton.html('<i class="fas fa-stop"></i>');
    recordingIndicator.removeClass("d-none");

    console.log("Recording started");
  } catch (error) {
    console.error("Error accessing microphone:", error);
    alert(
      "Unable to access microphone. Please check your browser permissions.",
    );
  }
}

/**
 * Stop recording audio
 */
async function stopRecording() {
  if (isRecording) {
    isRecording = false;

    // Disconnect and close
    recorder.disconnect();
    audioInput.disconnect();

    // Process audio data
    const leftchannel = recorder.leftchannel;
    const recordingLength = leftchannel.reduce(
      (acc, buf) => acc + buf.length,
      0,
    );

    // Flatten buffer
    const samples = flattenArray(leftchannel, recordingLength);

    // Encode to WAV
    const sampleRate = audioContext.sampleRate;
    const audioBlob = encodeWAV(samples, sampleRate);

    await sendAudioToServer(audioBlob);

    // Stop stream tracks
    const stream = audioInput.mediaStream;
    if (stream) stream.getTracks().forEach((track) => track.stop());

    await audioContext.close();

    // Update UI
    micButton.removeClass("recording");
    micButton.html('<i class="fas fa-microphone"></i>');
    recordingIndicator.addClass("d-none");

    console.log("Recording stopped");
  }
}

// Helper: Flatten buffer array
function flattenArray(channelBuffer, recordingLength) {
  const result = new Float32Array(recordingLength);
  let offset = 0;
  for (let i = 0; i < channelBuffer.length; i++) {
    const buffer = channelBuffer[i];
    result.set(buffer, offset);
    offset += buffer.length;
  }
  return result;
}

// Helper: Writes string to DataView
function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i));
  }
}

// Helper: Encode WAV
function encodeWAV(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  /* RIFF identifier */
  writeString(view, 0, "RIFF");
  /* RIFF chunk length */
  view.setUint32(4, 36 + samples.length * 2, true);
  /* RIFF type */
  writeString(view, 8, "WAVE");
  /* format chunk identifier */
  writeString(view, 12, "fmt ");
  /* format chunk length */
  view.setUint32(16, 16, true);
  /* sample format (raw) */
  view.setUint16(20, 1, true);
  /* channel count */
  view.setUint16(22, 1, true);
  /* sample rate */
  view.setUint32(24, sampleRate, true);
  /* byte rate (sample rate * block align) */
  view.setUint32(28, sampleRate * 2, true);
  /* block align (channel count * bytes per sample) */
  view.setUint16(32, 2, true);
  /* bits per sample */
  view.setUint16(34, 16, true);
  /* data chunk identifier */
  writeString(view, 36, "data");
  /* data chunk length */
  view.setUint32(40, samples.length * 2, true);

  floatTo16BitPCM(view, 44, samples);

  return new Blob([view], { type: "audio/wav" });
}

// Helper: Float to 16-bit PCM
function floatTo16BitPCM(output, offset, input) {
  for (let i = 0; i < input.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, input[i]));
    output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }
}

/**
 * Send audio to server for speech-to-text conversion
 */
async function sendAudioToServer(audioBlob) {
  showLoading(true);

  try {
    // Convert blob to array buffer
    const audioData = await audioBlob.arrayBuffer();

    // Send to server
    const response = await fetch("/speech-to-text", {
      method: "POST",
      headers: {
        "Content-Type": "audio/wav",
      },
      body: audioData,
    });

    const data = await response.json();

    if (data.text && data.text !== "null") {
      // Display transcribed message
      displayMessage(data.text, "user");

      // Process message
      await processMessage(data.text);
    } else {
      displayMessage(
        "Sorry, I couldn't understand that. Please try again.",
        "assistant",
      );
    }
  } catch (error) {
    console.error("Error sending audio:", error);
    displayMessage(
      "Sorry, there was an error processing your audio.",
      "assistant",
    );
  } finally {
    showLoading(false);
  }
}

/**
 * Process message through OpenAI and get response
 */
async function processMessage(message) {
  showLoading(true);

  try {
    const selectedVoice = voiceSelect.val();

    const response = await fetch("/process-message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userMessage: message,
        voice: selectedVoice,
      }),
    });

    const data = await response.json();

    if (data.openaiResponseText) {
      // Display assistant response
      displayMessage(data.openaiResponseText, "assistant");

      // Play audio response if available
      if (data.openaiResponseSpeech) {
        playAudioResponse(data.openaiResponseSpeech);
      }
    } else {
      displayMessage("Sorry, I couldn't process your request.", "assistant");
    }
  } catch (error) {
    console.error("Error processing message:", error);
    displayMessage(
      "Sorry, there was an error processing your message.",
      "assistant",
    );
  } finally {
    showLoading(false);
  }
}

/**
 * Display message in chat
 */
function displayMessage(text, sender) {
  const messageDiv = $("<div>").addClass("message");

  if (sender === "user") {
    messageDiv.addClass("user-message");
    messageDiv.html(`
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="message-content">
                <p>${escapeHtml(text)}</p>
            </div>
        `);
  } else {
    messageDiv.addClass("assistant-message");
    messageDiv.html(`
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>${escapeHtml(text)}</p>
            </div>
        `);
  }

  chatMessages.append(messageDiv);

  // Scroll to bottom
  scrollToBottom();
}

/**
 * Play audio response
 */
function playAudioResponse(base64Audio) {
  try {
    // Stop any currently playing audio
    stopAudioPlayback();

    // Convert base64 to audio
    const audioData = atob(base64Audio);
    const arrayBuffer = new ArrayBuffer(audioData.length);
    const view = new Uint8Array(arrayBuffer);

    for (let i = 0; i < audioData.length; i++) {
      view[i] = audioData.charCodeAt(i);
    }

    const audioBlob = new Blob([arrayBuffer], { type: "audio/wav" });
    const audioUrl = URL.createObjectURL(audioBlob);

    currentAudio = new Audio(audioUrl);

    // Update state and UI
    isSpeaking = true;
    micButton.addClass("speaking");
    micButton.html('<i class="fas fa-stop"></i>');

    currentAudio.play();

    // Clean up
    currentAudio.onended = () => {
      stopAudioPlayback();
      URL.revokeObjectURL(audioUrl);
    };
  } catch (error) {
    console.error("Error playing audio:", error);
    stopAudioPlayback();
  }
}

/**
 * Stop audio playback
 */
function stopAudioPlayback() {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
  }

  isSpeaking = false;
  micButton.removeClass("speaking");

  // Revert icon based on recording state (should be idle if we were speaking)
  if (!isRecording) {
    micButton.html('<i class="fas fa-microphone"></i>');
  }
}

/**
 * Toggle between light and dark theme
 */
function toggleTheme() {
  $("body").toggleClass("dark-theme");

  // Update icon
  if ($("body").hasClass("dark-theme")) {
    themeToggle.html('<i class="fas fa-sun"></i>');
    localStorage.setItem("theme", "dark");
  } else {
    themeToggle.html('<i class="fas fa-moon"></i>');
    localStorage.setItem("theme", "light");
  }
}

/**
 * Load saved theme preference
 */
function loadTheme() {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "dark") {
    $("body").addClass("dark-theme");
    themeToggle.html('<i class="fas fa-sun"></i>');
  }
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
  if (show) {
    loadingOverlay.removeClass("d-none");
  } else {
    loadingOverlay.addClass("d-none");
  }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
  const chatContainer = $(".chat-container");
  chatContainer.scrollTop(chatContainer[0].scrollHeight);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

/**
 * Handle Enter key in input field
 */
messageInput.on("keypress", function (e) {
  if (e.which === 13 && !e.shiftKey) {
    e.preventDefault();
    messageForm.submit();
  }
});

console.log("Script loaded successfully");
