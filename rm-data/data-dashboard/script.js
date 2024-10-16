// Sample data for charts
const barChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
        label: 'Sales',
        data: [12, 19, 3, 5, 2, 3, 10],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
    }]
};

const lineChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
        label: 'Website Visitors',
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
    }]
};

const pieChartData = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
        label: 'Color Preferences',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)'
        ],
        borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
    }]
};

const doughnutChartData = {
    labels: ['Direct', 'Organic Search', 'Referral', 'Social Media'],
    datasets: [{
        label: 'Traffic Sources',
        data: [30, 50, 15, 5],
        backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
        ],
        borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 1
    }]
};

// Create charts
window.onload = function() {
    const barChart = new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: barChartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Sales'
                }
            }
        }
    });

    const lineChart = new Chart(document.getElementById('lineChart'), {
        type: 'line',
        data: lineChartData,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Website Visitors'
                }
            }
        }
    });

    const pieChart = new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: pieChartData,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Color Preferences'
                }
            }
        }
    });

    const doughnutChart = new Chart(document.getElementById('doughnutChart'), {
        type: 'doughnut',
        data: doughnutChartData,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Traffic Sources'
                }
            }
        }
    });
};