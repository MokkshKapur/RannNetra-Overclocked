import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const AnalyticsSection = () => {
  const [chartData, setChartData] = useState({
    labels: ['Zone-1', 'Zone-51', 'Range-22', 'Range-12', 'Front', 'Zone-17', ''],
    datasets: [
      {
        label: 'Hotspots',
        data: [65, 59, 80, 81, 56, 55, 40],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Casualties',
        data: [28, 48, 40, 19, 86, 27, 34],
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  });

  useEffect(() => {
    // Fetch data from API and update chartData
    // For now, using static data
  }, []);

  return (
    <div style={{ color: 'white', background: 'linear-gradient(to right,rgb(11, 25, 39),rgb(6, 22, 65))', padding: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)' }}>
      <h2>Analytics Section 📊</h2>
      <Bar data={chartData} />
    </div>
  );
};

export default AnalyticsSection;
