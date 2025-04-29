import struct

def hex_to_float(hex_str):
    return struct.unpack('!f', bytes.fromhex(hex_str))[0]

def parse_vector_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    total_tests = 0
    passed = 0
    failed = 0
    test_num = 1

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("vector_length:"):
            vec_len = int(line.split(":")[1].strip())
            patch = []
            filter_ = []

            print(f"\n=== Test {test_num} ===")
            print(f"Vector Length: {vec_len}")
            i += 1

            for _ in range(vec_len):
                patch_hex, filter_hex = lines[i].strip().split()
                patch_val = hex_to_float(patch_hex)
                filter_val = hex_to_float(filter_hex)
                patch.append(patch_val)
                filter_.append(filter_val)
                print(f"patch = {patch_val:.6f}, filter = {filter_val:.6f} → product = {patch_val * filter_val:.6f}")
                i += 1

            dut_line = lines[i].strip()
            assert dut_line.startswith("DUT:"), f"Expected DUT line, got {dut_line}"
            dut_result = hex_to_float(dut_line.split(":")[1].strip())
            i += 1  # skip blank line
            i += 1

            sw_result = sum(p * f for p, f in zip(patch, filter_))

            print(f"\n[Software Result]  : {sw_result:.6f}")
            print(f"[DUT Result]       : {dut_result:.6f}")

            if abs(sw_result - dut_result) < 1e-3:
                print("[RESULT] ✅ PASS")
                passed += 1
            else:
                print("[RESULT] ❌ FAIL")
                failed += 1

            total_tests += 1
            test_num += 1
        else:
            i += 1

    print("\n--- Scoreboard ---")
    print(f"Total Tests : {total_tests}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("------------------")

if __name__ == "__main__":
    parse_vector_file("dot_product_vectors.txt")
