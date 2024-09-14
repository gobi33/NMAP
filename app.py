from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    ip_address = request.form['ipAddress']
    try:
        # Run nmap scan command to scan all ports and get service versions
        nmap_output = subprocess.run(['nmap', '-p-', '-sV', ip_address], capture_output=True, text=True)
        
        # Extract open ports and their services
        open_ports = re.findall(r'(\d+)\/(tcp|udp)\s+(open)\s+(.*?)\n', nmap_output.stdout)
        
        # Render result.html with scan details
        return render_template('result.html', ip_address=ip_address, open_ports=open_ports, scan_result=nmap_output.stdout)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
