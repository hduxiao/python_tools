// face_detect.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <filesystem>
#include <Windows.h>
#include "libfacedetection/facedetectcnn.h"

#pragma warning(push,0)
#include <opencv2/opencv.hpp>
#pragma warning(pop)

// link opencv
#ifdef _DEBUG
#pragma comment(lib, "opencv_world454d.lib")
#else
#pragma comment(lib, "opencv_world454.lib")
#endif // _DEBUG

class TimeCounter
{
public:
	TimeCounter()
	{
		LARGE_INTEGER freq{};
		QueryPerformanceFrequency(&freq);
		m_freqInv = 1.0 / freq.QuadPart;
	}
	inline void StartCount() { QueryPerformanceCounter(&m_startTime); }
	inline void EndCount()
	{
		QueryPerformanceCounter(&m_endTime);
		m_current = (m_endTime.QuadPart - m_startTime.QuadPart) * m_freqInv;
		m_totalTime += m_current;
		++m_counter;
	}
	inline double GetCurrent() { return m_current * 1000; }
	inline double GetAverage() { return m_totalTime / m_counter * 1000; }
	inline double GetFPS() { return m_counter / m_totalTime; }
	void StandardPrint(const char* info) { printf("[%lld][%s]cur: %.2lf, avg: %.2lf, fps: %.2lf\n", m_counter, info, GetCurrent(), GetAverage(), GetFPS()); }
	void ShowConsole()
	{
		FILE* stream;
		AllocConsole();
		freopen_s(&stream, "CONOUT$", "w", stdout);
		if (!::IsWindowVisible(::GetConsoleWindow()))
		{
			::ShowWindow(::GetConsoleWindow(), SW_SHOW);
		}
	}
private:
	LARGE_INTEGER m_startTime{ 0 };
	LARGE_INTEGER m_endTime{ 0 };
	LONGLONG m_counter{ 0 };
	double m_totalTime{ 0.0 };
	double m_freqInv{ 0.0 };
	double m_current{ 0.0 };
};

static bool doMosaic(cv::Mat img, int msize = 7)
{
	for (int i = 0; i < img.cols - msize; i += msize)
		for (int j = 0; j < img.rows - msize; j += msize)
		{
			cv::Rect r = cv::Rect(i, j, msize, msize);
			cv::Mat mosaic = img(r);
			mosaic.setTo(cv::mean(mosaic));
		}
	return true;
}

int main(int argc, char* argv[])
{
	if (argc != 2)
	{
		printf("please input a video!\n");
		return 0;
	}

	std::string input_video_path(argv[1]);
	if (std::filesystem::exists(input_video_path) != true)
	{
		printf("video not exist!\n");
		return 0;
	}

	std::string output_path = input_video_path + "facedetect.mp4";

	void* result_buffer = malloc(0x20000);

	TimeCounter counter;

	cv::VideoCapture video_cap(input_video_path);

	double fps = video_cap.get(cv::CAP_PROP_FPS);
	//int height = video_cap.get(cv::CAP_PROP_FRAME_HEIGHT);
	//int width = video_cap.get(cv::CAP_PROP_FRAME_WIDTH);
	int height = 240;
	int width = 320;
	cv::Size frame_size = cv::Size(width, height);
	int frame_count = video_cap.get(cv::CAP_PROP_FRAME_COUNT);
	int fourcc = { cv::CAP_OPENCV_MJPEG };

	cv::VideoWriter video_writer(output_path, fourcc, fps, frame_size);

	cv::Mat sample;
	cv::Mat output;
	for (int i = 0; i < frame_count; i++)
	{
		counter.StartCount();

		video_cap >> sample;
		if (sample.empty())
		{
			break;
		}

		cv::resize(sample, output, frame_size);

		void* bgr3_data = output.data;
		int* pcount = facedetect_cnn((unsigned char*)result_buffer, (unsigned char*)bgr3_data, width, height, width * 3);
		printf("detect faces num: %d\n", *pcount);

		for (int i = 0; i < *pcount; i++)
		{
			//copy data
			short* p = ((short*)((unsigned char*)result_buffer + 4)) + 142 * size_t(i);
			float score = (float)p[0];
			printf("detect score: %f\n", score);
			int x = (int)p[1];
			int y = (int)p[2];
			int w = (int)p[3];
			int h = (int)p[4];

			cv::Rect rect{};
			rect.x = x;
			rect.y = y;
			rect.width = w;
			rect.height = h;

			cv::Mat roi = output(rect);
			doMosaic(roi);

			//cv::rectangle(output, cv::Point(x, y), cv::Point(x + w, y + h), cv::Scalar(0, 255, 0));
			//cv::putText(output, std::to_string(score), cv::Point(x, y + 15), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0));

			printf("x: %d y: %d w: %d h: %d\n", x, y, w, h);
		}

		video_writer << output;

		printf("encode frame %d / %d\n", i + 1, frame_count);

		counter.EndCount();
		counter.StandardPrint("face detect");
		//break;
	}

	free(result_buffer);
}

