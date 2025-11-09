import { Link } from 'react-router-dom';
import { MessageSquare, CheckCircle, XCircle } from 'lucide-react';

const AdCard = ({ ad }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition">
      {/* Status Badge */}
      <div className="flex justify-between items-start mb-4">
        <span
          className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
            ad.is_active
              ? 'bg-green-100 text-green-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {ad.is_active ? (
            <CheckCircle className="w-4 h-4" />
          ) : (
            <XCircle className="w-4 h-4" />
          )}
          {ad.is_active ? 'Active' : 'Inactive'}
        </span>
      </div>

      {/* Ad Name */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{ad.ad_name}</h3>

      {/* Campaign and Adset Info */}
      <div className="space-y-2 text-sm text-gray-600 mb-4">
        {ad.campaign_name && (
          <div>
            <span className="font-medium">Campaign:</span> {ad.campaign_name}
          </div>
        )}
        {ad.adset_name && (
          <div>
            <span className="font-medium">Ad Set:</span> {ad.adset_name}
          </div>
        )}
        {ad.status && (
          <div>
            <span className="font-medium">Status:</span>{' '}
            <span className="uppercase">{ad.status}</span>
          </div>
        )}
      </div>

      {/* Template Status */}
      <div className="flex items-center gap-2 mb-4">
        <MessageSquare className="w-4 h-4 text-gray-500" />
        <span className="text-sm text-gray-600">
          {ad.has_template ? (
            <span className="text-green-600 font-medium">Template configured</span>
          ) : (
            <span className="text-orange-600 font-medium">No template</span>
          )}
        </span>
      </div>

      {/* Action Button */}
      <Link
        to={`/messages/edit?ad_id=${ad.id}`}
        className="block w-full text-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        {ad.has_template ? 'Edit Template' : 'Create Template'}
      </Link>
    </div>
  );
};

export default AdCard;
