import { useState, useEffect } from 'react';
import { Users, Calendar, CheckCircle, XCircle } from 'lucide-react';
import { Card } from '../components/Card';
import { Loading } from '../components/Loading';
import { ErrorMessage } from '../components/ErrorMessage';
import { attendanceAPI } from '../services/api';

export const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await attendanceAPI.getDashboard();
      setStats(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  const statCards = [
    {
      title: 'Total Employees',
      value: stats?.total_employees || 0,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      title: 'Attendance Records',
      value: stats?.total_attendance_records || 0,
      icon: Calendar,
      color: 'bg-purple-500',
    },
    {
      title: 'Present Today',
      value: stats?.present_today || 0,
      icon: CheckCircle,
      color: 'bg-green-500',
    },
    {
      title: 'Absent Today',
      value: stats?.absent_today || 0,
      icon: XCircle,
      color: 'bg-red-500',
    },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      <Card className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Welcome to HRMS Lite</h2>
        <p className="text-gray-600">
          This is a lightweight Human Resource Management System for managing employees and tracking attendance.
          Use the navigation above to manage employees and record attendance.
        </p>
      </Card>
    </div>
  );
};
