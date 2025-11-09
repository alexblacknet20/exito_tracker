import { useState } from 'react';
import { useAds, useSyncAds } from '../../hooks/useAds';
import AdCard from './AdCard';
import { RefreshCw } from 'lucide-react';

const AdsList = () => {
  const [filter, setFilter] = useState('all');

  const { data, isLoading, error } = useAds(
    filter === 'all' ? {} : { is_active: filter === 'active' }
  );

  const syncMutation = useSyncAds();

  const handleSync = async () => {
    try {
      const result = await syncMutation.mutateAsync();
      alert(result.message || 'Ads synced successfully!');
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to sync ads');
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Loading ads...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        Error loading ads: {error.message}
      </div>
    );
  }

  const ads = data?.data || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Facebook Ads</h2>
          <p className="text-gray-600 mt-1">
            {ads.length} {ads.length === 1 ? 'ad' : 'ads'} found
          </p>
        </div>
        <button
          onClick={handleSync}
          disabled={syncMutation.isPending}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
        >
          <RefreshCw
            className={`w-4 h-4 ${syncMutation.isPending ? 'animate-spin' : ''}`}
          />
          {syncMutation.isPending ? 'Syncing...' : 'Sync Ads'}
        </button>
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg transition ${
            filter === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('active')}
          className={`px-4 py-2 rounded-lg transition ${
            filter === 'active'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Active
        </button>
        <button
          onClick={() => setFilter('inactive')}
          className={`px-4 py-2 rounded-lg transition ${
            filter === 'inactive'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Inactive
        </button>
      </div>

      {/* Ads Grid */}
      {ads.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-500 text-lg">No ads found</p>
          <p className="text-gray-400 mt-2">
            Click "Sync Ads" to fetch ads from Facebook
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ads.map((ad) => (
            <AdCard key={ad.id} ad={ad} />
          ))}
        </div>
      )}
    </div>
  );
};

export default AdsList;
