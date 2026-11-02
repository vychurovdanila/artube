import { Link, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-6 h-20 flex items-center justify-between">
          {/* Логотип и меню */}
          <div className="flex items-center gap-10">
            <Link to="/" className="flex items-center gap-2">
              <span className="text-2xl font-black tracking-tighter text-black uppercase">AR<span className="text-blue-500">TUBE</span></span>
            </Link>
            <nav className="hidden md:flex gap-6 text-sm font-bold text-gray-500">
              <Link to="/" className="hover:text-black">FURNITURE</Link>
              <Link to="/" className="hover:text-black text-black">DECOR</Link>
              <Link to="/" className="hover:text-black">FINISHING</Link>
              <Link to="/" className="hover:text-black text-blue-600">COMPLECTS</Link>
            </nav>
          </div>

          {/* Поиск и кнопки */}
          <div className="flex items-center gap-4">
            <div className="relative hidden lg:block">
              <input type="text" placeholder="Search" className="pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-md text-sm w-64 focus:outline-none focus:border-blue-500" />
              <svg className="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>

            {user && (
              <Link to="/upload" className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2.5 rounded-md text-sm font-bold transition-colors">
                UPLOAD
              </Link>
            )}

            {user ? (
              <div className="flex items-center gap-3">
                <Link to="/profile" className="w-10 h-10 rounded-md bg-gray-100 flex items-center justify-center overflow-hidden border border-gray-200">
                  {user.avatar_url ? <img src={user.avatar_url} alt="Avatar" className="w-full h-full object-cover" /> : <span className="text-sm font-bold text-gray-500">{user.name.charAt(0)}</span>}
                </Link>
                <button onClick={logout} className="text-sm font-semibold text-gray-500 hover:text-black">Выйти</button>
              </div>
            ) : (
              <Link to="/login" className="text-sm font-bold text-black hover:text-blue-500">Войти</Link>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1 w-full max-w-[1600px] mx-auto px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
