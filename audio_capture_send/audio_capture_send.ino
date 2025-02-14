#include <driver/i2s.h>
#include <WiFi.h>

// INMP441 Microphone Pin Configuration
#define I2S_WS  15  // Word Select (L/R Clock)
#define I2S_SCK 14  // Bit Clock (BCLK)
#define I2S_SD  32  // Serial Data (DOUT)
#define SAMPLE_RATE 16000  // Sampling rate (16kHz)

// WiFi AP Configuration
const char* ssid = "ESP32_Audio_AP";
const char* password = "123456789";

WiFiServer server(80);  // Create a TCP server on port 80

void setup() {
    Serial.begin(9600);

    // Configure I2S
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_I2S_MSB,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 64,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };

    i2s_pin_config_t pin_config = {
        .bck_io_num = I2S_SCK,      // BCLK
        .ws_io_num = I2S_WS,        // L/R Clock
        .data_out_num = I2S_PIN_NO_CHANGE, // Not used (Output, set to NO_CHANGE)
        .data_in_num = I2S_SD       // Data Input
    };

    // Install and start I2S driver
    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config);

    // Start WiFi AP
    WiFi.softAP(ssid, password);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);

    // Start the TCP server
    server.begin();
    Serial.println("TCP server started");
}

void loop() {
    int16_t sampleBuffer[1024]; // Buffer for audio samples
    size_t bytesRead;
    
    // Read data from the microphone
    i2s_read(I2S_NUM_0, sampleBuffer, sizeof(sampleBuffer), &bytesRead, portMAX_DELAY);

    // Calculate average amplitude
    long sum = 0;
    int numSamples = bytesRead / sizeof(int16_t);

    for (int i = 0; i < numSamples; i++) {
        sum += abs(sampleBuffer[i]); // Get absolute value of the signal
    }

    int averageAmplitude = sum / numSamples;

    Serial.println(averageAmplitude); // Print amplitude value

    // Check for client connections
    WiFiClient client = server.available();
    if (client) {
        Serial.println("New client connected");
        
        // Send the average amplitude to the client
        client.write((uint8_t*)sampleBuffer, bytesRead);

        
        // Close the connection
        client.stop();
        Serial.println("Client disconnected");
    }

    delay(20);
}