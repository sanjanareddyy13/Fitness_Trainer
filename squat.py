import cv2
import mediapipe as mp
import numpy as np
import imageio
import json
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def landmark_coord(landmark):
    return np.array([landmark.x, landmark.y])

def find_angle(a, b, c):
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def start(goal):
    goal = int(goal)
    orig_goal = goal
    # For webcam input:
    is_up = True
    is_mid = False
    down_count = 0
    up_count = 0
    mid_count = 0
    rep_count = 0
    up_angle = 160
    up_distance = -1
    mid_distance = 0
    half_rep = False
    half_rep_percent = 0
    percentage = 0

    gif = imageio.mimread('./countdown_images/squat_visual.gif')

    gif_frame = 0
    start_text_frames = 0

    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(cv2.CAP_PROP_FPS)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    frames = 0
    countdown = 3
    countdown_complete = False
    start_countdown = False
    print("ready...")

    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            image = cv2.flip(image, 1)
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if cv2.waitKey(1) == ord(' '):
                start_countdown = True

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if start_countdown and not countdown_complete:

                font_scale = 7
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_thickness = 24

                countdown_text = str(countdown)
                text_size, _ = cv2.getTextSize(countdown_text, font, font_scale, font_thickness)
                text_size_x, text_size_y = text_size

                image = cv2.putText(image, countdown_text, ((width - text_size_x) // 2, (height + text_size_y) // 2),
                                    font,
                                    font_scale, (0, 0, 0), font_thickness + 8, cv2.LINE_AA)

                image = cv2.putText(image, countdown_text, ((width - text_size_x) // 2, (height + text_size_y) // 2),
                                    font,
                                    font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

                frames += 1
                if frames >= fps:
                    if countdown <= 1:
                        countdown_complete = True
                        print("start!")
                    else:

                        frames = 0
                        print(countdown)
                        countdown -= 1

                    # Flip the image horizontally for a selfie-view display.

            if not start_countdown:
                gif_image = cv2.cvtColor(gif[math.floor(gif_frame)], cv2.COLOR_BGR2RGB)

                gif_image = cv2.resize(
                    gif_image, (image.shape[1], image.shape[0]))

                image = cv2.addWeighted(image, 0.5, gif_image, 0.5, 0)

                countdown_text = "Press space to start the countdown!"
                text_size, _ = cv2.getTextSize(countdown_text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)
                text_size_x, text_size_y = text_size

                image = cv2.putText(image, countdown_text,
                                    ((width - text_size_x) // 2, (height - (4 * text_size_y)) // 2),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    2, (0, 0, 0), 3, cv2.LINE_AA)

            if countdown_complete and start_text_frames != -1:
                start_text_frames += 1
                font_scale = 4
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_thickness = 14

                countdown_text = "Start!"
                text_size, _ = cv2.getTextSize(
                    countdown_text, font, font_scale, font_thickness)
                text_size_x, text_size_y = text_size
                image = cv2.putText(image, countdown_text, ((width - text_size_x) // 2, (height + text_size_y) // 2),
                                    font,
                                    font_scale, (0, 0, 0), font_thickness + 8, cv2.LINE_AA)
                image = cv2.putText(image, countdown_text, ((width - text_size_x) // 2, (height + text_size_y) // 2),
                                    font,
                                    font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
                if start_text_frames >= (fps // 2):
                    start_text_frames = -1

            if half_rep is True:
                font_scale = 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_thickness = 2

                percent_text = "Half-rep: " + \
                    str(round(half_rep_percent, 2)) + "% there"
                text_size, _ = cv2.getTextSize(
                    percent_text, font, font_scale, font_thickness)
                text_size_x, text_size_y = text_size

                iimage = cv2.putText(image, percent_text, ((width - text_size_x) // 2, (height + text_size_y) // 6), font,
                                font_scale, (0, 0, 0), font_thickness + 6, cv2.LINE_AA)
                image = cv2.putText(image, percent_text, ((width - text_size_x) // 2, (height + text_size_y) // 6), font,
                                font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
            if start_countdown:
                font_scale = 2
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_thickness = 10
                goal_text = "Squats left: " + str(goal) if goal > 0 else "Goal completed!"
                if goal < 0:
                    goal_text = goal_text + " +" + str(-1 * goal)
                text_size, _ = cv2.getTextSize(goal_text, font, font_scale, font_thickness)
                text_size_x, text_size_y = text_size

                image = cv2.putText(image, goal_text, ((width - text_size_x) // 2, (height - (2 * text_size_y))), font,
                                    font_scale, (0, 0, 0), 7, cv2.LINE_AA)

                image = cv2.putText(image, goal_text, ((width - text_size_x) // 2, (height - (2 * text_size_y))), font,
                                    font_scale, (255, 255, 255), 3, cv2.LINE_AA)

            length = width * 3 / 4 * percentage / 100
            top_left = (int((width - length) / 2), int(18 / 20 * height))
            bottom_right = (int(width - ((width - length) / 2)), int(19 / 20 * height))
            color = (0, int(255 * percentage / 100), 0)
            thickness = -1

            if length > 0:
                image = cv2.rectangle(image, top_left, bottom_right, color, thickness)

            escape_text = "Hold esc to finish"
            text_size, _ = cv2.getTextSize(escape_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_size_x, text_size_y = text_size

            image = cv2.putText(image, escape_text, (1, int(1.5 * text_size_y)),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 0), 5, cv2.LINE_AA)
            image = cv2.putText(image, escape_text, (1, int(1.5 * text_size_y)),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Main image', image)

            gif_frame += 0.25
            if gif_frame >= len(gif):
                gif_frame = 0

            if results.pose_landmarks is not None and countdown_complete:
                # Extract pose landmarks
                landmarks = results.pose_landmarks.landmark

                left_hip = landmark_coord(
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
                left_knee = landmark_coord(
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
                left_heel = landmark_coord(
                    landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value])
                left_angle = find_angle(left_hip, left_knee, left_heel)

                right_hip = landmark_coord(
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
                right_knee = landmark_coord(
                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
                right_heel = landmark_coord(
                    landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value])
                right_angle = find_angle(right_hip, right_knee, right_heel)

                if (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z <
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z):
                    test_hip = left_hip
                    test_knee = left_knee
                    test_angle = left_angle
                else:
                    test_hip = right_hip
                    test_knee = right_knee
                    test_angle = right_angle

                if test_knee[1] <= test_hip[1] + up_distance / 4:
                    down_count += 1
                    if down_count >= int(fps / 6):
                        is_up = False
                        up_count = 0

                if test_angle >= up_angle:
                    up_count += 1
                    up_distance = test_knee[1] - test_hip[1]
                    if up_count >= int(fps / 6):
                        if is_up is False:
                            rep_count += 1
                            goal -= 1
                            print(rep_count)
                            half_rep = False
                        if is_up is True and is_mid is True:
                            half_rep = True
                            half_rep_percent = (
                                1 - mid_distance / up_distance) * 100
                        is_up = True
                        down_count = 0
                        is_mid = False
                        mid_count = 0
                        mid_distance = up_distance

                if test_angle < up_angle and test_knee[1] > test_hip[1]:
                    mid_distance = min(
                        mid_distance, test_knee[1] - test_hip[1])
                    mid_count += 1
                    if mid_count >= int(fps / 6):
                        is_mid = True
                        up_count = 0

                percentage = (1 - ((test_knee[1] - test_hip[1]) / up_distance)) * 100
                percentage = max(percentage, 0)
                percentage = min(percentage, 100)

            if cv2.waitKey(5) & 0xFF == 27:  # esc to quit
                with open('results.json', 'r') as f:
                    data = json.load(f)
                    data[3].append(rep_count)
                    data[3].append(orig_goal)

                with open('results.json', 'w') as f:
                    json.dump(data, f)
                break
    cap.release()
    cv2.destroyAllWindows()
