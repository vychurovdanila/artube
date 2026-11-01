import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';

export default function Profile() {
  const { user, loading } = useAuth();

  if (loading) return <div className="text-center mt-20">Загрузка...</div>;
  if (!user) return <Navigate to="/login" />;

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-8 rounded-xl shadow-sm border border-gray-100">
      <div className="flex items-center gap-6 mb-8">
        <div className="w-24 h-24 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden border-2 border-blue-500">
          {user.avatar_url ? <img src={user.avatar_url} alt="Avatar" className="w-full h-full object-cover" /> : <span className="text-3xl font-black text-gray-400">{user.name.charAt(0)}</span>}
        </div>
        <div>
          <h1 className="text-2xl font-black">{user.name}</h1>
          <p className="text-gray-500">{user.email || user.telegram_username || 'Telegram user'}</p>
          <span className="inline-block mt-2 px-3 py-1 bg-blue-50 text-blue-600 text-xs font-bold rounded-full uppercase tracking-wide">
            {user.role}
          </span>
        </div>
      </div>
    </div>
  );
}
