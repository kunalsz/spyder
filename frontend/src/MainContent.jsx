import React, { useEffect, useRef, useState } from 'react';

import { Network, DataSet } from 'vis-network/standalone';

import 'vis-network/styles/vis-network.css';



const MainContent = ({ selectedData }) => {

  const networkRef = useRef(null);

  const networkInstanceRef = useRef(null);

  const nodesRef = useRef([]);

  const edgesRef = useRef([]);

  const collapsedNodesRef = useRef(new Set());

  const [error, setError] = useState(null);



  const createNetwork = () => {

    try {

      const container = networkRef.current;

      if (!container) {

        setError('Network container not found');

        return;

      }



      // Reset nodes and edges

      nodesRef.current = [];

      edgesRef.current = [];



      // Recursive node creation function

      const createNode = (item, key, parentId = null, level = 0) => {

        if (!item) return null;



        const node = {

          id: key,

          label: item.label || key,

          title: item.path || 'No path',

          level: level,

          hidden: false,

          parentId: parentId

        };



        nodesRef.current.push(node);



        // Add edge if parent exists

        if (parentId) {

          edgesRef.current.push({ 

            from: parentId, 

            to: key,

            hidden: false 

          });

        }



        // Recursively process sub-items

        if (item.subItems && Object.keys(item.subItems).length > 0) {

          Object.entries(item.subItems).forEach(([subKey, subItem]) => {

            createNode(subItem, subKey, key, level + 1);

          });

        }



        return node;

      };



      // Create nodes starting from the selected data

      createNode(selectedData, '1');



      // Create network

      const nodes = new DataSet(nodesRef.current);

      const edges = new DataSet(edgesRef.current);



      const options = {

          layout: {

              improvedLayout: false // Disable automatic optimization for a cleaner circular effect

          },

          physics: {

              enabled: true,

              solver: "repulsion", // Creates a circular-like distribution

              repulsion: {

                  centralGravity: 0.2, // Strength of gravity toward the center

                  springLength: 150, // Ideal length of edges

                  springConstant: 0.05

              }

          },

          nodes: {

              shape: 'dot',

              size: 15,

              font: {

                  size: 16

              },

              color: {

                  background: '#2a9d8f',

                  border: '#264653',

                  highlight: {

                      background: '#e76f51',

                      border: '#264653'

                  }

              }

          },

          edges: {

              smooth: true,

              color: '#7A7A7A',

              arrows: {

                  to: { enabled: false } // Disable arrows for a clean circular look

              }

          }

      };



      // Destroy existing network if it exists

      if (networkInstanceRef.current) {

        networkInstanceRef.current.destroy();

      }



      // Create new network instance

      networkInstanceRef.current = new Network(container, { nodes, edges }, options);



      // Add double-click event for collapsing/expanding

      networkInstanceRef.current.on('doubleClick', (params) => {

        if (params.nodes.length > 0) {

          const nodeId = params.nodes[0];

          toggleNodeChildren(nodeId, nodes, edges);

        }

      });



      //single click event to show card

      



    } catch (error) {

      console.error('Network creation error:', error);

      setError(error.message);

    }

  };



  // Function to toggle child nodes visibility

  const toggleNodeChildren = (parentNodeId, nodes, edges) => {

    // Find all children of the clicked node

    const findChildren = (parentId) => {

      return nodesRef.current.filter(node => node.parentId === parentId)

        .map(node => node.id);

    };



    const childrenIds = findChildren(parentNodeId);



    // Check if we're collapsing or expanding

    const isCollapsing = !collapsedNodesRef.current.has(parentNodeId);



    // Toggle visibility of direct children

    childrenIds.forEach(childId => {

      // Update node visibility

      nodes.update({ 

        id: childId, 

        hidden: isCollapsing 

      });



      // Recursively hide/show nested children if collapsing

      if (isCollapsing) {

        const nestedChildrenIds = findChildren(childId);

        nestedChildrenIds.forEach(nestedChildId => {

          nodes.update({ 

            id: nestedChildId, 

            hidden: true 

          });

        });

      }

    });



    // Track collapsed state

    if (isCollapsing) {

      collapsedNodesRef.current.add(parentNodeId);

    } else {

      collapsedNodesRef.current.delete(parentNodeId);

    }

  };



  // Create network when selectedData changes

  useEffect(() => {

    if (selectedData) {

      createNetwork();

    }

  }, [selectedData]);



  // Error rendering

  if (error) {

    return (

      <div className="bg-red-100 text-red-800 p-4">

        <h2>Error Initializing Network</h2>

        <p>{error}</p>

      </div>

    );

  }



  return (

    <div className="w-full h-screen">

      <div 

        ref={networkRef} 

        className="w-full h-full" 

        style={{ 

          minHeight: '500px', 

          backgroundColor: 'rgba(0,0,0,0.1)' 

        }} 

      />

    </div>

  );

};



export default MainContent;