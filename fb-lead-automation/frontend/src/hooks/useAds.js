import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import adsService from '../services/adsService';

/**
 * Hook for fetching all ads
 * @param {Object} params - Query parameters
 */
export const useAds = (params = {}) => {
  return useQuery({
    queryKey: ['ads', params],
    queryFn: () => adsService.getAll(params),
  });
};

/**
 * Hook for fetching specific ad
 * @param {number} id - Ad ID
 */
export const useAd = (id) => {
  return useQuery({
    queryKey: ['ads', id],
    queryFn: () => adsService.getById(id),
    enabled: !!id,
  });
};

/**
 * Hook for syncing ads from Facebook
 */
export const useSyncAds = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: adsService.sync,
    onSuccess: () => {
      // Invalidate and refetch ads
      queryClient.invalidateQueries({ queryKey: ['ads'] });
    },
  });
};

/**
 * Hook for deleting an ad
 */
export const useDeleteAd = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id) => adsService.delete(id),
    onSuccess: () => {
      // Invalidate and refetch ads
      queryClient.invalidateQueries({ queryKey: ['ads'] });
    },
  });
};
