import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import Catalog from './pages/Catalog';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Upload from './pages/Upload';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Catalog />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="profile" element={<Profile />} />
            <Route path="upload" element={<Upload />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}