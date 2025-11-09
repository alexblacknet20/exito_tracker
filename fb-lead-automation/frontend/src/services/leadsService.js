import api from './api';

const leadsService = {
  /**
   * Get all leads with pagination
   * @param {Object} params - Query parameters (page, per_page)
   * @returns {Promise}
   */
  getAll: async (params = {}) => {
    const response = await api.get('/api/leads', { params });
    return response.data;
  },

  /**
   * Get specific lead by ID
   * @param {number} id - Lead ID
   * @returns {Promise}
   */
  getById: async (id) => {
    const response = await api.get(`/api/leads/${id}`);
    return response.data;
  },

  /**
   * Get lead statistics
   * @returns {Promise}
   */
  getStats: async () => {
    const response = await api.get('/api/leads/stats');
    return response.data;
  },
};

export default leadsService;
