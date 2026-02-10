import { Loader2 } from 'lucide-react';

export const Loading = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className="w-8 h-8 animate-spin text-primary-600 mb-2" />
      <p className="text-gray-600">{message}</p>
    </div>
  );
};
