import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import MainContent from './MainContent';
import data from '../../saved_data/save.json';

const App = () => {
  // Initialize selectedData with the root item from the JSON
  const [selectedData, setSelectedData] = useState(data['1'] || data);

  return (
    <>
      <header className="p-4 shadow-mg border-2 border-gray-900 text-center bg-gray-800 text-white">
        <h1 className="text-3xl font-bold headline-dark">My Hierarchical Project</h1>
      </header>
      <div className="flex h-screen dark">
        <Sidebar data={data} onLinkClick={setSelectedData} />
        <MainContent selectedData={selectedData} />
      </div>
    </>
  );
};

export default App;