using UnityEngine;
using UnityEngine.UI;

public class ImageLoader : MonoBehaviour
{
    public Texture2D[] textures;
    [SerializeField] private Slider seasonSlider;

    void Awake()
    {
        // Load all textures in Resources/LARGE_bloom_maps/
        textures = Resources.LoadAll<Texture2D>("LARGE_bloom_maps");
        Debug.Log($"Loaded {textures.Length} textures.");
        seasonSlider.maxValue = textures.Length - 1;
    }
}
