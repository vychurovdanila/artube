import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../api/client';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const body = new URLSearchParams();
      body.append('username', email);
      body.append('password', password);

      const data = await apiFetch<{ access_token: string }>('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
      });
      await login(data.access_token);
      navigate('/profile');
    } catch (err: any) {
      setError(err.message || 'Ошибка входа');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 bg-white p-8 rounded-xl shadow-sm border border-gray-100">
      <h1 className="text-2xl font-black mb-6">Вход</h1>
      {error && <div className="mb-4 text-red-500 text-sm font-semibold">{error}</div>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required className="px-4 py-3 border border-gray-200 rounded-md focus:outline-none focus:border-blue-500" />
        <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} required className="px-4 py-3 border border-gray-200 rounded-md focus:outline-none focus:border-blue-500" />
        <button type="submit" className="bg-blue-500 text-white font-bold py-3 rounded-md hover:bg-blue-600">Войти</button>
      </form>
      <p className="mt-6 text-center text-sm text-gray-500">Нет аккаунта? <Link to="/register" className="text-blue-500 font-bold hover:underline">Регистрация</Link></p>
    </div>
  );
}
