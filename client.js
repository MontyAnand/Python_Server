const net = require('net');
const client1 = new net.Socket();
const host = '127.0.0.1'; // Replace with the server's IP address
const port = 8888; // Replace with the server's port

client1.connect(port, host, () => {
    console.log('client1 Connected to server');
    client1.write(JSON.stringify({
        protocol:1,
        companyId : 'AAPL',
        frame:'1Min'
    }));
    setInterval(()=>{
        client1.write(JSON.stringify({
            protocol:0,
            companyId:'AAPL',
            frame:'1Min',
            open:Math.random()*1000,
            high:Math.random()*1000,
            low:Math.random()*1000,
            close:Math.random()*1000,
            volume:Math.random()*100000000
        }));
    },2000);
    
});

// Receive data from the server
client1.on('data', (data) => {
    console.log('Received to client1: ' + data);
    // Close the connection
});

// Handle connection closure
client1.on('close', () => {
    console.log('client1 Connection closed');
});

// Handle errors
client1.on('error', (err) => {
    console.error('Connection error on client1: ' + err);
});
