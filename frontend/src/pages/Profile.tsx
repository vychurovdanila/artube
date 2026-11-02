import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';
import { apiFetch } from '../api/client';

export default function Profile() {
  const { user, loading } = useAuth();

  if (loading) return <div className="text-center mt-20">Загрузка...</div>;
  if (!user) return <Navigate to="/login" />;

  const handleBecomeAuthor = async () => {
    await apiFetch('/api/users/me/become-author', { method: 'POST' });
    window.location.reload(); // Простой способ обновить контекст
  };

  const handleBecomePartner = async () => {
    await apiFetch('/api/users/me/become-partner', { method: 'POST' });
    window.location.reload();
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-8 rounded-xl shadow-sm border border-gray-100">
      <div className="flex items-center gap-6 mb-8">
        <div className="w-24 h-24 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden border-2 border-blue-500">
          {user.avatar_url ? <img src={user.avatar_url} alt="Avatar" className="w-full h-full object-cover" /> : <span className="text-3xl font-black text-gray-400">{user.name.charAt(0)}</span>}
        </div>
        <div>
          <h1 className="text-2xl font-black">{user.name}</h1>
          <p className="text-gray-500">{user.email || user.telegram_username || 'Telegram user'}</p>
          <div className="flex flex-wrap gap-2 mt-2">
            {user.roles.map(r => (
              <span key={r} className="inline-block px-3 py-1 bg-blue-50 text-blue-600 text-xs font-bold rounded-full uppercase tracking-wide">
                {r}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-8 flex gap-4 border-t pt-6">
        {!user.roles.includes('author') && (
          <button onClick={handleBecomeAuthor} className="px-4 py-2 border border-blue-500 text-blue-500 rounded font-bold hover:bg-blue-50">
            Стать автором
          </button>
        )}
        {!user.roles.includes('partner') && (
          <button onClick={handleBecomePartner} className="px-4 py-2 border border-gray-500 text-gray-700 rounded font-bold hover:bg-gray-50">
            Стать партнером (дизайнером)
          </button>
        )}
      </div>
    </div>
  );
}
