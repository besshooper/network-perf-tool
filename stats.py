import numpy as np # type: ignore

# calculates P99 or P95 latency threshold from intervals
# recorded in iperf3's JSON output. Ignores first interval
# due to higher test start-up jitter.
# returns tuple (P95 jitter, P99 jitter)
def calculate_latency_threshold(data):
    jitter_samples = []

    # Iterate through intervals, starting from the second interval
    ints = data['intervals']
    for i in range(1, len(ints)):

        jitter_samples.append(ints[i]['sum']['jitter_ms'])
    # Calculate the P95 and P99 thresholds
    p95_jitter = np.percentile(jitter_samples, 95)
    p99_jitter = np.percentile(jitter_samples, 99)

    return p95_jitter, p99_jitter

# Calculates average RTT from the intervals recorded in 
# iperf3's output. Ignores first interval due to excessive
# test startup latency
def calculate_average_rtt(data):
    rtt_samples = []

    # Iterate through intervals, starting from the second interval
    ints = data['intervals']
    for i in range(1, len(ints)):
        # This structure may vary, but RTT is usually in the 'streams' array
        rtt = ints[i]['streams'][0]['rtt']
        rtt_samples.append(rtt)

    # Calculate the new, clean average
    clean_avg_rtt = sum(rtt_samples) / len(rtt_samples)

    return clean_avg_rtt