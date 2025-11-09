import api from './api';

const messagesService = {
  /**
   * Get all message templates
   * @returns {Promise}
   */
  getAll: async () => {
    const response = await api.get('/api/messages');
    return response.data;
  },

  /**
   * Get specific message template
   * @param {number} id - Template ID
   * @returns {Promise}
   */
  getById: async (id) => {
    const response = await api.get(`/api/messages/${id}`);
    return response.data;
  },

  /**
   * Create new message template
   * @param {Object} data - Template data
   * @returns {Promise}
   */
  create: async (data) => {
    const response = await api.post('/api/messages', data);
    return response.data;
  },

  /**
   * Update existing message template
   * @param {number} id - Template ID
   * @param {Object} data - Updated template data
   * @returns {Promise}
   */
  update: async (id, data) => {
    const response = await api.put(`/api/messages/${id}`, data);
    return response.data;
  },

  /**
   * Delete message template
   * @param {number} id - Template ID
   * @returns {Promise}
   */
  delete: async (id) => {
    const response = await api.delete(`/api/messages/${id}`);
    return response.data;
  },

  /**
   * Preview template with sample data
   * @param {number} id - Template ID
   * @param {Object} leadData - Sample lead data
   * @returns {Promise}
   */
  preview: async (id, leadData) => {
    const response = await api.post(`/api/messages/${id}/preview`, { lead_data: leadData });
    return response.data;
  },
};

export default messagesService;
