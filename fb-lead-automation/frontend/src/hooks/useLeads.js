import { useQuery } from '@tanstack/react-query';
import leadsService from '../services/leadsService';

/**
 * Hook for fetching all leads
 * @param {Object} params - Query parameters (page, per_page)
 */
export const useLeads = (params = {}) => {
  return useQuery({
    queryKey: ['leads', params],
    queryFn: () => leadsService.getAll(params),
  });
};

/**
 * Hook for fetching specific lead
 * @param {number} id - Lead ID
 */
export const useLead = (id) => {
  return useQuery({
    queryKey: ['leads', id],
    queryFn: () => leadsService.getById(id),
    enabled: !!id,
  });
};

/**
 * Hook for fetching lead statistics
 */
export const useLeadStats = () => {
  return useQuery({
    queryKey: ['leads', 'stats'],
    queryFn: leadsService.getStats,
  });
};
