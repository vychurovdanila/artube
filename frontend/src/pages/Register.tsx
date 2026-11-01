import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { apiFetch } from '../api/client';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('author');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await apiFetch('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, name, role }),
      });
      navigate('/login');
    } catch (err: any) {
      setError(err.message || 'Ошибка регистрации');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-white p-8 rounded-xl shadow-sm border border-gray-100">
      <h1 className="text-2xl font-black mb-6">Регистрация</h1>
      {error && <div className="mb-4 text-red-500 text-sm font-semibold">{error}</div>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <select value={role} onChange={e => setRole(e.target.value)} className="px-4 py-3 border border-gray-200 rounded-md bg-white">
          <option value="author">Я Автор</option>
          <option value="designer">Я Дизайнер</option>
          <option value="client">Я Покупатель (B2C)</option>
        </select>
        <input type="text" placeholder="Имя" value={name} onChange={e => setName(e.target.value)} required className="px-4 py-3 border border-gray-200 rounded-md focus:outline-none focus:border-blue-500" />
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required className="px-4 py-3 border border-gray-200 rounded-md focus:outline-none focus:border-blue-500" />
        <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} required minLength={8} className="px-4 py-3 border border-gray-200 rounded-md focus:outline-none focus:border-blue-500" />
        <button type="submit" className="bg-blue-500 text-white font-bold py-3 rounded-md hover:bg-blue-600">Создать аккаунт</button>
      </form>
      <p className="mt-6 text-center text-sm text-gray-500">Уже есть аккаунт? <Link to="/login" className="text-blue-500 font-bold hover:underline">Войти</Link></p>
    </div>
  );
}
