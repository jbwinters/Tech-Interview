import ActivityDashboard from './components/ActivityDashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-6">
          <h1 className="text-3xl font-bold">Greenhouse Activity Tracker</h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <ActivityDashboard />
        </div>
      </main>
      <footer className="mt-10 py-4 text-center text-sm text-gray-500">
        &copy; {new Date().getFullYear()} Greenhouse Inc.
      </footer>
    </div>
  );
}

export default App;
