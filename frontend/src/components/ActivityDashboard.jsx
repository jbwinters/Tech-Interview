import React, { useState, useEffect } from 'react';

const ActivityDashboard = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const endActivity = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/activities/${id}/end`, {
        method: 'PUT'
      });
      const updated = await response.json();
      setActivities(activities.map(a => 
        a.id === updated.id ? a : updated 
      ));
    } catch (err) {
      setError('Failed to end activity');
    }
  };

  useEffect(() => {
    // TODO: Implement actual fetch logic
    setLoading(false); 
  }, []);

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Active Workers</h2>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : activities.length === 0 ? (
        <p className="text-gray-500">No activities found.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {activities.map(activity => (
            <div key={activity.id} className="border border-gray-200 p-4 rounded-lg shadow-sm bg-gray-50">
              <h3 className="text-lg font-medium mb-2">{activity.type}</h3>
              <p className="text-sm text-gray-700 mb-1">
                Location: {activity.location.zone} - Row {activity.location.row}
              </p>
              <p className="text-sm text-gray-700 mb-3">Workers: {activity.worker_ids.length}</p>
              {!activity.end_time && (
                <button 
                  onClick={() => endActivity(activity.id)}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  End Activity
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ActivityDashboard;
