<template>
  <div class="ai-chat-container">
    <van-nav-bar title="AI Chat" fixed />
    
    <div class="chat-content">
      <div class="messages-container" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant' && message.content === ''" class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div v-else v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>
      
      <div class="input-container">
        <van-field
          v-model="userInput"
          rows="1"
          autosize
          type="textarea"
          placeholder="Ask a question..."
          class="chat-input"
          @keypress.enter.prevent="sendMessage"
        />
        <van-button 
          type="primary" 
          class="send-button" 
          :disabled="isLoading || !userInput.trim()" 
          @click="sendMessage"
        >
          Send
        </van-button>
      </div>
    </div>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import TabBar from '../components/TabBar.vue';
import { showToast } from 'vant';
import * as marked from 'marked';
import DOMPurify from 'dompurify';
import { aiChatConfig } from '../config/api';

const messages = ref([
  { role: 'assistant', content: 'Ask me to summarize a story, explain context, or draft a quick brief.' }
]);
const userInput = ref('');
const messagesContainer = ref(null);
const isLoading = ref(false);

const chatEndpoint = ref(aiChatConfig.chatEndpoint);
const model = ref(aiChatConfig.model);

const formatMessage = (content) => {
  if (!content) return '';
  return DOMPurify.sanitize(marked.parse(content));
};

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;
  
  const userMessage = userInput.value.trim();
  messages.value.push({ role: 'user', content: userMessage });
  userInput.value = '';
  
  messages.value.push({ role: 'assistant', content: '' });
  
  await nextTick();
  scrollToBottom();
  
  isLoading.value = true;
  try {
    await fetchAIResponse(userMessage);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    messages.value[messages.value.length - 1].content = `Error: ${error.message || 'Please check the network connection and AI settings.'}`;
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

const fetchAIResponse = async (userMessage) => {
  const allMessages = messages.value
    .slice(0, -1)
    .map(msg => ({ role: msg.role, content: msg.content }));
  
  try {
    const response = await fetch(chatEndpoint.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: model.value,
        messages: allMessages
      })
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || error.detail || `HTTP error: ${response.status}`);
    }
    
    const result = await response.json();
    const aiResponse = result.data?.content;

    messages.value[messages.value.length - 1].content =
      aiResponse || 'Sorry, I could not generate a response. Please check the AI settings or try again later.';
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

watch(messages, () => {
  nextTick(scrollToBottom);
}, { deep: true });

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding-top: 46px;
  padding-bottom: 50px;
  box-sizing: border-box;
  background-color: var(--background-color);
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message {
  margin-bottom: 12px;
  max-width: 86%;
}

.user-message {
  margin-left: auto;
}

.ai-message {
  margin-right: auto;
}

.message-content {
  padding: 11px 13px;
  border-radius: 6px;
  word-break: break-word;
  font-size: 14px;
  line-height: 1.55;
}

.user-message .message-content {
  background-color: var(--primary-color);
  color: white;
}

.ai-message .message-content {
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  color: var(--text-color);
}

.input-container {
  display: flex;
  gap: 10px;
  padding: 10px 12px;
  border-top: 1px solid var(--border-color);
  background-color: var(--surface-color);
}

.chat-input {
  flex: 1;
  margin-right: 0;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

.send-button {
  align-self: flex-end;
  min-width: 68px;
  border-radius: 6px;
  font-weight: 800;
}

.message-content pre {
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.message-content code {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 4px;
  border-radius: 3px;
}

.message-content img {
  max-width: 100%;
}

.typing-indicator {
  display: flex;
  padding: 5px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: var(--text-color-lighter);
  border-radius: 50%;
  margin: 0 2px;
  display: inline-block;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

:deep(pre) {
  background-color: var(--muted-surface-color);
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

:deep(code) {
  font-family: monospace;
  background-color: var(--muted-surface-color);
  padding: 2px 4px;
  border-radius: 4px;
}

:deep(p) {
  margin: 8px 0;
}

:deep(ul), :deep(ol) {
  padding-left: 20px;
}

:deep(a) {
  color: var(--primary-color);
  text-decoration: none;
}
</style>
