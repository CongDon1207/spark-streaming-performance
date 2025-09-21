# exercise_skew_fill_gaps.py
# Bài tập Level 2: Xử lý Data Skew (Slide 30-31)
#
# Nhiệm vụ sinh viên:
# 1. Implement salting technique
# 2. Pre-aggregation trước khi shuffle
# 3. Tối ưu hóa partition strategy
# 4. Monitor và so sánh performance
#
# Scenario:
# - Dữ liệu bị skew theo user_id
# - Một số user_id có rất nhiều events
# - Cần phân phối đều workload
#
# Chỗ trống được đánh dấu bằng: # TODO: Implement here
#
# Kết quả mong đợi:
# - Giảm thời gian xử lý
# - Phân phối đều task duration
# - Không có straggler tasks