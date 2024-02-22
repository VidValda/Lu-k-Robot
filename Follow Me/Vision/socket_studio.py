import socket

class RaspberrySocket:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def send_data(self, data):
        data_str = str(data)
        self.sock.sendall(data_str.encode())

    def send_tracks(self,tracks,width_ratio,height_ratio):
        confirmed_tracks = [track for track in tracks if track.is_confirmed()]

        # Check if there are any confirmed tracks
        if confirmed_tracks:
            # Find the track with the minimum track_id
            min_track = min(confirmed_tracks, key=lambda track: track.track_id)


            left, top, right, bottom = min_track.to_ltrb()
            left, top, right, bottom = (left * width_ratio), (top * height_ratio), (right * width_ratio), (bottom * height_ratio)

            centroid_x = (right+left)/2 - 320
            bounding_box_area = 80000-(right-left) * (bottom-top)

            print("Centroid:", (round(centroid_x,2), round(bounding_box_area,2)))
            self.send_data(f"{round(centroid_x,2)};{round(bounding_box_area,2)}")
        else:
            print("No confirmed tracks to calculate the centroid.")
            self.send_data(f"{0};{0}")


    def close_connection(self):
        self.sock.close()
