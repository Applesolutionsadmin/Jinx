const SmeeClient = require('smee-client')

class SmeeClientClass {
  constructor(source, target, dataFetcher) {
    this.smee = new SmeeClient({
      source: source,
      target: target,
      logger: console
    });
    this.dataFetcher = dataFetcher;
  }

  start() {
    this.events = this.smee.start();
    this.events.on('message', (event) => {
      if (event.data) {
        this.dataFetcher.updateData(event.data);
      } else {
        this.dataFetcher.updateData('Nothing is available');
      }
    });
  }

  stop() {
    this.events.close();
  }
}

class DataFetcher {
  constructor(url, elementSelector) {
    this.url = url;
    this.element = document.querySelector(elementSelector);
  }

  async fetchData() {
    const response = await fetch(this.url);
    const data = await response.json();
    this.element.innerHTML = `<h1>Webhook Data</h1><table><tr><th>Data</th></tr>${data.map(row => `<tr><td>${row}</td></tr>`).join('')}</table>`;
  }

  startFetching(interval) {
    this.fetchData();
    this.intervalId = setInterval(() => this.fetchData(), interval);
  }

  stopFetching() {
    clearInterval(this.intervalId);
  }

  updateData(data) {
    this.element.innerHTML = `<h1>Webhook Data</h1><table><tr><th>Data</th></tr><tr><td>${data}</td></tr></table>`;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  const smeeClient = new SmeeClientClass('https://smee.io/Y6LOh5WKJjbCew38', 'http://localhost:8000');
  smeeClient.start();

  const dataFetcher = new DataFetcher('https://smee.io/Y6LOh5WKJjbCew38', 'header');
  dataFetcher.startFetching(5000);
});

// script.js
var worker = new Worker('worker.js');
worker.postMessage(data); // Send data to our worker