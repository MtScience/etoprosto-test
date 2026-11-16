import sys
import time
import urllib.error
import urllib.request


def measure_download_speed(url: str, num_requests: int = 10) -> None:
    total_bytes = 0
    total_duration = 0.0

    headers = {"User-Agent": "Mozilla/5.0 (compatible; SpeedTestScript/1.0)"}
    req = urllib.request.Request(url, headers=headers)

    for i in range(num_requests):
        try:
            start_time = time.perf_counter()

            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read()

            end_time = time.perf_counter()

            total_bytes += len(data)
            total_duration += end_time - start_time

        except urllib.error.URLError as e:
            print(f"Request {i + 1} failed: {e.reason}", file=sys.stderr)
        except Exception as e:
            print(f"Request {i + 1} encountered an error: {e}", file=sys.stderr)

    if total_duration == 0 or total_bytes == 0:
        print(
            "Error: No data was successfully downloaded.", file=sys.stderr
        )
        sys.exit(1)

    bytes_per_sec = total_bytes / total_duration
    mb_per_sec = bytes_per_sec / (1024 * 1024)  # Megabytes per second (MiB/s)
    mbps = (bytes_per_sec * 8) / 1_000_000  # Megabits per second (Mbps)

    print(f"Total Downloaded: {total_bytes:,} bytes")
    print(f"Total Time:       {total_duration:.4f} seconds")
    print(f"Average Speed:    {mbps:.2f} Mbps ({mb_per_sec:.2f} MB/s)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <URL>", file=sys.stderr)
        sys.exit(1)

    target_url = sys.argv[1]

    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    measure_download_speed(target_url, num_requests=10)
