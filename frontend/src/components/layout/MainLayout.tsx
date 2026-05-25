import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
const MainLayout: React.FC = () => {
  const { user, logout } = useAuth();
  return (
    <div className="drawer"><input id="my-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content"><div className="navbar bg-base-100"><div className="flex-1"><Link to="/dashboard" className="btn btn-ghost text-xl">DocVersion</Link></div>
        <div className="flex-none">{user && <span className="mr-2">{user.email}</span>}<button onClick={logout} className="btn btn-sm">Logout</button></div></div>
        <Outlet /></div>
      <div className="drawer-side"><label htmlFor="my-drawer" className="drawer-overlay"></label><ul className="menu p-4 w-80 bg-base-100"><li><Link to="/dashboard">Dashboard</Link></li><li><Link to="/smr">SMR Management</Link></li><li><Link to="/audit-logs">Audit Logs</Link></li></ul></div>
    </div>
  );
};
export default MainLayout;
