import cv2
import socket
import struct
import time
import ntplib

# Function to get NTP timestamp from a specific NTP server
def get_ntp_timestamp(ntp_server):
    client = ntplib.NTPClient()
    try:
        response = client.request(ntp_server, version=3)
        ntp_timestamp = response.tx_time
        seconds = int(ntp_timestamp)
        fractions = int((ntp_timestamp - seconds) * (1<<32))
        return seconds, fractions
    except Exception as e:
        print("Error querying NTP server:", e)
        return 0, 0

# Function to add NTP extension to RTP packet
def create_rtp_packet_with_ntp(frame_data, ntp_server):
    # RTP packet components (simplified)
    version = 2
    padding = 0
    extension = 1
    csrc_count = 0
    marker = 0
    payload_type = 96
    sequence_number = 0
    timestamp = int(time.time())
    ssrc = 12345

    # RTP header
    rtp_header = struct.pack("!BBHII", 
                             (version << 6) | (padding << 5) | (extension << 4) | csrc_count,
                             (marker << 7) | payload_type,
                             sequence_number,
                             timestamp,
                             ssrc)

    # NTP timestamp from specified server
    seconds, fractions = get_ntp_timestamp(ntp_server)
    extension_header = struct.pack("!HHII", 1, 2, seconds, fractions)
    
    # Combine RTP header, extension, and frame data
    rtp_packet = rtp_header + extension_header + frame_data
    return rtp_packet

# Function to capture frames from the Axis camera
def capture_frames_from_camera(rtsp_url, ntp_server):
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame (e.g., convert to bytes, compress, etc.)
        # This is a placeholder; actual processing depends on your requirements
        frame_data = cv2.imencode('.jpg', frame)[1].tobytes()

        # Create RTP packet with NTP timestamp from specific NTP server
        rtp_packet = create_rtp_packet_with_ntp(frame_data, ntp_server)

        # Send RTP packet over a network (omitted for brevity)
        # ...

    cap.release()

# Main function
def main():
    # RTSP URL of the Axis camera and NTP server address
    rtsp_url = "rtsp://root:pass@192.168.0.90/axis-media/media.amp"
    ntp_server = "192.168.0.91"
    
    capture_frames_from_camera(rtsp_url, ntp_server)

if __name__ == "__main__":
    main()

