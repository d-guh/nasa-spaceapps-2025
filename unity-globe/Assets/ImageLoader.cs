using UnityEngine;
using System.IO;
using System.Linq;

public class ImageFolderLoader : MonoBehaviour
{
    [Header("Assets")]
    public string folderPath = "LARGE_bloom_maps";   // e.g. "MyImages"
    public Texture2D[] loadedTextures;

    void Awake()
    {
        LoadImages();
    }

    public void LoadImages()
    {
        string fullPath = Path.Combine(Application.streamingAssetsPath, folderPath);

        if (!Directory.Exists(fullPath))
        {
            Debug.LogError($"Folder not found: {fullPath}");
            return;
        }

        // Get all supported image files (sorted alphabetically)
        string[] imagePaths = Directory.GetFiles(fullPath)
            .Where(f => f.EndsWith(".png") || f.EndsWith(".jpg") || f.EndsWith(".jpeg"))
            .OrderBy(f => f)
            .ToArray();

        if (imagePaths.Length == 0)
        {
            Debug.LogError($"No image files found in {fullPath}");
            return;
        }

        loadedTextures = new Texture2D[imagePaths.Length];

        for (int i = 0; i < imagePaths.Length; i++)
        {
            byte[] bytes = File.ReadAllBytes(imagePaths[i]);
            Texture2D tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            tex.LoadImage(bytes);
            tex.name = Path.GetFileNameWithoutExtension(imagePaths[i]);
            loadedTextures[i] = tex;
        }

        Debug.Log($"Loaded {loadedTextures.Length} textures from {fullPath}");
    }
}
