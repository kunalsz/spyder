import React from 'react';

const Sidebar = ({ data, onLinkClick }) => {

  const handleLinkClick = (item) => {
    onLinkClick(item); 
  };

  return (
    <div className="bg-gray-800 text-white  md:w-1/5 h-screen p-4 overflow-y-auto">

      <div className="md:block block">
        {Object.keys(data).map((key) => (
          <div key={key} className="my-2">
            <button
              className="hover:bg-gray-600   bg-gray-900 w-full p-2 rounded transition-transform transform hover:scale-105"
              onClick={() => handleLinkClick(data[key])}
            >
              {data[key].path}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
