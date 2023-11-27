import cv2
import socket
import struct
import time

# Function to create NTP timestamp
def create_ntp_timestamp():
    current_time = time.time()
    ntp_epoch = 2208988800
    ntp_timestamp = current_time + ntp_epoch
    seconds = int(ntp_timestamp)
    fractions = int((ntp_timestamp - seconds) * (1<<32))
    return seconds, fractions

# Function to add NTP extension to RTP packet
def create_rtp_packet_with_ntp(frame_data):
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

    # NTP timestamp extension
    seconds, fractions = create_ntp_timestamp()
    extension_header = struct.pack("!HHII", 1, 2, seconds, fractions)
    
    # Combine RTP header, extension, and frame data
    rtp_packet = rtp_header + extension_header + frame_data
    return rtp_packet

# Function to capture frames from the Axis camera
def capture_frames_from_camera(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get the current time as the timestamp for the frame
        frame_timestamp = time.time()

        # Print the frame timestamp
        print("Frame Timestamp:", frame_timestamp)

        # Process the frame (e.g., convert to bytes, compress, etc.)
        frame_data = frame.tobytes()

        # Create RTP packet with NTP timestamp
        rtp_packet = create_rtp_packet_with_ntp(frame_data)

        # Send RTP packet over a network (omitted for brevity)
        # ...

    cap.release()

# Main function
def main():
    # RTSP URL of the Axis camera (replace with actual URL)
    rtsp_url = "rtsp://root:pass@192.168.0.90/axis-media/media.amp"
    
    capture_frames_from_camera(rtsp_url)

if __name__ == "__main__":
    main()

