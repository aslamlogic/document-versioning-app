import React, { createContext, useState, useContext, ReactNode } from 'react';
import axios from 'axios';
interface AuthContextType { user: any; login: (email: string, password: string) => Promise<void>; logout: () => void; }
const AuthContext = createContext<AuthContextType | undefined>(undefined);
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState(null);
  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams(); formData.append('email', email); formData.append('password', password);
    const res = await axios.post('/api/auth/login', formData);
    localStorage.setItem('token', res.data.access_token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access_token}`;
    const me = await axios.get('/api/auth/me');
    setUser(me.data);
  };
  const logout = () => { localStorage.removeItem('token'); delete axios.defaults.headers.common['Authorization']; setUser(null); };
  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>;
};
export const useAuth = () => { const ctx = useContext(AuthContext); if (!ctx) throw new Error('useAuth must be used within AuthProvider'); return ctx; };
