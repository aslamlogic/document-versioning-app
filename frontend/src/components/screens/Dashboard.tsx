import React, { useEffect, useState } from 'react';
import axios from 'axios';
const Dashboard: React.FC = () => {
  const [docs, setDocs] = useState([]);
  useEffect(() => { axios.get('/api/documents').then(res => setDocs(res.data)); }, []);
  return (
    <div className="p-4"><h1 className="text-2xl font-bold">Documents</h1>
      <button className="btn btn-primary my-2">New Document</button>
      <div className="overflow-x-auto"><table className="table"><thead><tr><th>Name</th><th>Created</th></tr></thead>
      <tbody>{docs.map(doc => (<tr key={doc.id}><td>{doc.name}</td><td>{doc.created_at}</td></tr>))}</tbody></table></div>
    </div>
  );
};
export default Dashboard;
