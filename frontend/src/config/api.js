const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export const apiConfig = {
  baseURL,
}

export const aiChatConfig = {
  chatEndpoint: `${baseURL}/api/ai/chat`,
  model: import.meta.env.VITE_AI_MODEL || 'qwen3-max-preview',
}
