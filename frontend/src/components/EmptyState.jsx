import { FileX } from 'lucide-react';

export const EmptyState = ({ message = 'No data found', icon: Icon = FileX }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-gray-500">
      <Icon className="w-12 h-12 mb-3 text-gray-400" />
      <p className="text-lg">{message}</p>
    </div>
  );
};
