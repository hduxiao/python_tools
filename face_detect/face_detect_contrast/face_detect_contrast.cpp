#define _CRT_SECURE_NO_WARNINGS

// opencv
#pragma warning(push,0)
#include <opencv2/opencv.hpp>
#pragma warning(pop)
#ifdef _DEBUG
#pragma comment(lib, "opencv_world454d.lib")
#else
#pragma comment(lib, "opencv_world454.lib")
#endif // _DEBUG
// opencv

#include <filesystem>
#include <iostream>

struct Box
{
	int x;
	int y;
	int w;
	int h;
};

void add_box_to_image(std::vector<Box> Boxs, cv::Mat image)
{

}

int main()
{
	std::string gt_data_path{ "C:\\Users\\NERO\\Desktop\\wider_face_val_bbx_gt.txt" };

	FILE* gt_data_handle{ nullptr };
	gt_data_handle = fopen(gt_data_path.c_str(), "r");

	const char filename[1024]{};
	int face_count{};
	std::vector<Box> Boxs;

	do
	{
		// clear boxs
		std::vector<Box>().swap(Boxs);

		int ret1 = fscanf(gt_data_handle, "%s", filename);
		if (ret1 != 1)
		{
			break;
		}

		int ret2 = fscanf(gt_data_handle, "%d", &face_count);
		if (ret2 != 1)
		{
			break;
		}

		for (int i = 0; i < face_count; i++)
		{
			Box box{};

			int num[10]{};
			for (int j = 0; j < 10; j++)
			{
				int ret3 = fscanf(gt_data_handle, "%d", &num[j]);
				if (ret3 != 1)
				{
					break;
				}
			}

			box.x = num[0];
			box.y = num[1];
			box.w = num[2];
			box.h = num[3];

			Boxs.push_back(box);
		}

		std::cout << Boxs.size() << std::endl;
		break;
	} while (1);

}
