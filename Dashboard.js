import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell, LineChart, Line } from 'recharts';

const data = [
  {
    name: 'Custom',
    total_emissions: 0.00761076684818244,
    emissions_efficiency: 0.00001522153369636488,
    processing_time: 407.7881555557251,
    memory_usage: 20.042522430419922,
    cpu_utilization: 5.7,
    yearly_projections: 2.7779298995865904
  },
  {
    name: 'Pandas',
    total_emissions: 0.002565834622757236,
    emissions_efficiency: 0.000005131669245514471,
    processing_time: 164.36221861839294,
    memory_usage: 8.691791534423828,
    cpu_utilization: 5.4,
    yearly_projections: 0.936529637306391
  },
  {
    name: 'Polar',
    total_emissions: 0.0006309870101863992,
    emissions_efficiency: 0.0000012619740203727984,
    processing_time: 43.59013915061951,
    memory_usage: 17.273731231689453,
    cpu_utilization: 16.875,
    yearly_projections: 0.2303102587180357
  }
];

const calculatePercentageDifference = (value1, value2) => {
  return ((value1 - value2) / value2 * 100).toFixed(2);
};

const calculateYearlyImpact = (emissions, runsPerDay) => {
  return emissions * runsPerDay * 365;
};

const EmissionsComparison = ({ data }) => {
  const colors = ['#ef4444', '#3b82f6', '#22c55e'];
  const customEmissions = data.find(d => d.name === 'Custom').total_emissions;
  const pandasEmissions = data.find(d => d.name === 'Pandas').total_emissions;
  const polarEmissions = data.find(d => d.name === 'Polar').total_emissions;

  const customVsPolar = calculatePercentageDifference(customEmissions, polarEmissions);
  const customVsPandas = calculatePercentageDifference(customEmissions, pandasEmissions);
  const pandasVsPolar = calculatePercentageDifference(pandasEmissions, polarEmissions);

  return (
    <div className="space-y-4">
      <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4" role="alert">
        <p className="font-bold">Emissions Comparison Highlights:</p>
        <p>• Custom emits {customVsPolar}% more CO2 than Polar</p>
        <p>• Custom emits {customVsPandas}% more CO2 than Pandas</p>
        <p>• Pandas emits {pandasVsPolar}% more CO2 than Polar</p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis label={{ value: 'Emissions (kg CO₂)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="total_emissions" name="Total Emissions">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const EmissionsEfficiencyComparison = ({ data }) => {
  const colors = ['#ef4444', '#3b82f6', '#22c55e'];
  
  return (
    <div className="space-y-4">
      <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mb-4" role="alert">
        <p className="font-bold">Emissions Efficiency Comparison:</p>
        <p>Lower values indicate better efficiency (less emissions per million rows processed)</p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis label={{ value: 'Emissions per Million Rows (kg CO₂)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="emissions_efficiency" name="Emissions Efficiency">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const YearlyImpactComparison = ({ data }) => {
  const colors = ['#ef4444', '#3b82f6', '#22c55e'];
  const runsPerDay = 50;
  const yearlyImpactData = data.map(d => ({
    name: d.name,
    yearlyEmissions: calculateYearlyImpact(d.total_emissions, runsPerDay)
  }));

  const yearlyDataPoints = Array.from({length: 12}, (_, i) => {
    const month = i + 1;
    return {
      month: month,
      Custom: (yearlyImpactData.find(d => d.name === 'Custom').yearlyEmissions / 12) * month,
      Pandas: (yearlyImpactData.find(d => d.name === 'Pandas').yearlyEmissions / 12) * month,
      Polar: (yearlyImpactData.find(d => d.name === 'Polar').yearlyEmissions / 12) * month
    };
  });

  return (
    <div className="space-y-4">
      <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-4" role="alert">
        <p className="font-bold">Yearly Impact Projection (50 runs per day):</p>
        <p>• Custom: {yearlyImpactData.find(d => d.name === 'Custom').yearlyEmissions.toFixed(2)} kg CO₂</p>
        <p>• Pandas: {yearlyImpactData.find(d => d.name === 'Pandas').yearlyEmissions.toFixed(2)} kg CO₂</p>
        <p>• Polar: {yearlyImpactData.find(d => d.name === 'Polar').yearlyEmissions.toFixed(2)} kg CO₂</p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={yearlyDataPoints} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" label={{ value: 'Month', position: 'insideBottom', offset: -5 }} />
          <YAxis label={{ value: 'Cumulative Emissions (kg CO₂)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Custom" stroke={colors[0]} />
          <Line type="monotone" dataKey="Pandas" stroke={colors[1]} />
          <Line type="monotone" dataKey="Polar" stroke={colors[2]} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const ExecutionTimeComparison = ({ data }) => {
  const colors = ['#ef4444', '#3b82f6', '#22c55e'];
  const customTime = data.find(d => d.name === 'Custom').processing_time;
  const pandasTime = data.find(d => d.name === 'Pandas').processing_time;
  const polarTime = data.find(d => d.name === 'Polar').processing_time;

  const customVsPolar = calculatePercentageDifference(customTime, polarTime);
  const customVsPandas = calculatePercentageDifference(customTime, pandasTime);
  const pandasVsPolar = calculatePercentageDifference(pandasTime, polarTime);

  return (
    <div className="space-y-4">
      <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 mb-4" role="alert">
        <p className="font-bold">Execution Time Comparison Highlights:</p>
        <p>• Custom is {customVsPolar}% slower than Polar</p>
        <p>• Custom is {customVsPandas}% slower than Pandas</p>
        <p>• Pandas is {pandasVsPolar}% slower than Polar</p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis label={{ value: 'Execution Time (seconds)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="processing_time" name="Execution Time">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const ResourceUsage = ({ data }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Resource Usage Comparison</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis dataKey="name" type="category" />
          <Tooltip />
          <Legend />
          <Bar dataKey="memory_usage" name="Memory Usage (GB)" fill="#8884d8" />
          <Bar dataKey="cpu_utilization" name="CPU Utilization (%)" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const Dashboard = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-8">Advanced Data Processing Methods Comparison</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Emissions Comparison</h2>
          <EmissionsComparison data={data} />
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Emissions Efficiency Comparison</h2>
          <EmissionsEfficiencyComparison data={data} />
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Yearly Impact Projection</h2>
          <YearlyImpactComparison data={data} />
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Execution Time Comparison</h2>
          <ExecutionTimeComparison data={data} />
        </div>

        <div className="md:col-span-2">
          <ResourceUsage data={data} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;