import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
const Login: React.FC = () => {
  const [email, setEmail] = useState(''); const [password, setPassword] = useState('');
  const { login } = useAuth(); const navigate = useNavigate();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try { await login(email, password); navigate('/dashboard'); } catch (err) { alert('Login failed'); }
  };
  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200">
      <div className="card w-96 bg-base-100 shadow-xl">
        <div className="card-body"><h2 className="card-title">Document Versioning System</h2>
          <form onSubmit={handleSubmit}><input type="email" placeholder="Email" className="input input-bordered w-full mb-2" value={email} onChange={e=>setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" className="input input-bordered w-full mb-2" value={password} onChange={e=>setPassword(e.target.value)} required />
          <button type="submit" className="btn btn-primary w-full">Login</button></form>
        </div>
      </div>
    </div>
  );
};
export default Login;
