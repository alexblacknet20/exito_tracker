import api from './api';

const adsService = {
  /**
   * Get all ads with optional filtering
   * @param {Object} params - Query parameters
   * @returns {Promise}
   */
  getAll: async (params = {}) => {
    const response = await api.get('/api/ads', { params });
    return response.data;
  },

  /**
   * Get specific ad by ID
   * @param {number} id - Ad ID
   * @returns {Promise}
   */
  getById: async (id) => {
    const response = await api.get(`/api/ads/${id}`);
    return response.data;
  },

  /**
   * Manually sync ads from Facebook
   * @returns {Promise}
   */
  sync: async () => {
    const response = await api.post('/api/ads/sync');
    return response.data;
  },

  /**
   * Delete ad from database
   * @param {number} id - Ad ID
   * @returns {Promise}
   */
  delete: async (id) => {
    const response = await api.delete(`/api/ads/${id}`);
    return response.data;
  },
};

export default adsService;
