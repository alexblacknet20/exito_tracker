import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import messagesService from '../services/messagesService';

/**
 * Hook for fetching all message templates
 */
export const useMessages = () => {
  return useQuery({
    queryKey: ['messages'],
    queryFn: messagesService.getAll,
  });
};

/**
 * Hook for fetching specific message template
 * @param {number} id - Template ID
 */
export const useMessage = (id) => {
  return useQuery({
    queryKey: ['messages', id],
    queryFn: () => messagesService.getById(id),
    enabled: !!id,
  });
};

/**
 * Hook for creating a message template
 */
export const useCreateMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => messagesService.create(data),
    onSuccess: () => {
      // Invalidate and refetch messages
      queryClient.invalidateQueries({ queryKey: ['messages'] });
    },
  });
};

/**
 * Hook for updating a message template
 */
export const useUpdateMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }) => messagesService.update(id, data),
    onSuccess: () => {
      // Invalidate and refetch messages
      queryClient.invalidateQueries({ queryKey: ['messages'] });
    },
  });
};

/**
 * Hook for deleting a message template
 */
export const useDeleteMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id) => messagesService.delete(id),
    onSuccess: () => {
      // Invalidate and refetch messages
      queryClient.invalidateQueries({ queryKey: ['messages'] });
    },
  });
};

/**
 * Hook for previewing a message template
 */
export const usePreviewMessage = () => {
  return useMutation({
    mutationFn: ({ id, leadData }) => messagesService.preview(id, leadData),
  });
};
