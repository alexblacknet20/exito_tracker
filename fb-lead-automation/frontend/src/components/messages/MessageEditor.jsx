import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useAd } from '../../hooks/useAds';
import { useMessages, useCreateMessage, useUpdateMessage } from '../../hooks/useMessages';
import { ArrowLeft, Plus, Trash2, Eye } from 'lucide-react';

const MessageEditor = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const adId = searchParams.get('ad_id');

  const { data: adData } = useAd(adId);
  const { data: messagesData } = useMessages();
  const createMutation = useCreateMessage();
  const updateMutation = useUpdateMessage();

  const [templateName, setTemplateName] = useState('');
  const [messageText, setMessageText] = useState('');
  const [customVariables, setCustomVariables] = useState([]);
  const [preview, setPreview] = useState('');

  // Find existing template for this ad
  const existingTemplate = messagesData?.data?.find(
    (msg) => msg.ad_id === parseInt(adId)
  );

  useEffect(() => {
    if (existingTemplate) {
      setTemplateName(existingTemplate.template_name);
      setMessageText(existingTemplate.message_text);

      // Convert variables object to array
      const vars = existingTemplate.variables || {};
      const varsArray = Object.entries(vars).map(([key, value]) => ({ key, value }));
      setCustomVariables(varsArray);
    }
  }, [existingTemplate]);

  // Update preview when message or variables change
  useEffect(() => {
    generatePreview();
  }, [messageText, customVariables]);

  const addPlaceholder = (placeholder) => {
    setMessageText((prev) => prev + `{{${placeholder}}}`);
  };

  const addCustomVariable = () => {
    setCustomVariables([...customVariables, { key: '', value: '' }]);
  };

  const updateCustomVariable = (index, field, value) => {
    const updated = [...customVariables];
    updated[index][field] = value;
    setCustomVariables(updated);
  };

  const removeCustomVariable = (index) => {
    setCustomVariables(customVariables.filter((_, i) => i !== index));
  };

  const generatePreview = () => {
    let previewText = messageText;

    // Replace standard placeholders
    const sampleData = {
      first_name: 'John',
      last_name: 'Doe',
      email: 'john.doe@example.com',
      phone: '+1234567890',
    };

    Object.entries(sampleData).forEach(([key, value]) => {
      previewText = previewText.replace(new RegExp(`{{${key}}}`, 'g'), value);
    });

    // Replace custom variables
    customVariables.forEach(({ key, value }) => {
      if (key && value) {
        previewText = previewText.replace(new RegExp(`{{${key}}}`, 'g'), value);
      }
    });

    setPreview(previewText);
  };

  const handleSave = async () => {
    if (!templateName || !messageText) {
      alert('Please fill in template name and message text');
      return;
    }

    // Convert custom variables array to object
    const variablesObj = {};
    customVariables.forEach(({ key, value }) => {
      if (key) variablesObj[key] = value;
    });

    const data = {
      ad_id: parseInt(adId),
      template_name: templateName,
      message_text: messageText,
      variables: variablesObj,
    };

    try {
      if (existingTemplate) {
        await updateMutation.mutateAsync({ id: existingTemplate.id, data });
        alert('Template updated successfully!');
      } else {
        await createMutation.mutateAsync(data);
        alert('Template created successfully!');
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to save template');
    }
  };

  if (!adId) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        No ad selected. Please select an ad first.
      </div>
    );
  }

  const ad = adData?.data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate('/ads')}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            {existingTemplate ? 'Edit' : 'Create'} Message Template
          </h2>
          {ad && <p className="text-gray-600 mt-1">Ad: {ad.ad_name}</p>}
        </div>
      </div>

      {/* Editor */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        {/* Template Name */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Template Name
          </label>
          <input
            type="text"
            value={templateName}
            onChange={(e) => setTemplateName(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Welcome Message"
          />
        </div>

        {/* Message Text */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Message Text
          </label>
          <textarea
            value={messageText}
            onChange={(e) => setMessageText(e.target.value)}
            rows={6}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
            placeholder="Type your message here... Use {{placeholders}} for personalization"
          />
        </div>

        {/* Placeholder Buttons */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Insert Placeholders
          </label>
          <div className="flex flex-wrap gap-2">
            {['first_name', 'last_name', 'email', 'phone'].map((placeholder) => (
              <button
                key={placeholder}
                onClick={() => addPlaceholder(placeholder)}
                className="px-3 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition text-sm"
              >
                {`{{${placeholder}}}`}
              </button>
            ))}
          </div>
        </div>

        {/* Custom Variables */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium text-gray-700">
              Custom Variables
            </label>
            <button
              onClick={addCustomVariable}
              className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700"
            >
              <Plus className="w-4 h-4" />
              Add Variable
            </button>
          </div>
          <div className="space-y-2">
            {customVariables.map((variable, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={variable.key}
                  onChange={(e) => updateCustomVariable(index, 'key', e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="Variable name (e.g., product_name)"
                />
                <input
                  type="text"
                  value={variable.value}
                  onChange={(e) => updateCustomVariable(index, 'value', e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  placeholder="Default value"
                />
                <button
                  onClick={() => removeCustomVariable(index)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Preview */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <Eye className="w-4 h-4 text-gray-700" />
            <label className="block text-sm font-medium text-gray-700">Preview</label>
          </div>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 min-h-24">
            <p className="text-gray-800 whitespace-pre-wrap">{preview || 'Preview will appear here...'}</p>
          </div>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSave}
          disabled={createMutation.isPending || updateMutation.isPending}
          className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-medium"
        >
          {createMutation.isPending || updateMutation.isPending
            ? 'Saving...'
            : existingTemplate
            ? 'Update Template'
            : 'Create Template'}
        </button>
      </div>
    </div>
  );
};

export default MessageEditor;
