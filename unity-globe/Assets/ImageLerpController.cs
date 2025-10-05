using UnityEngine;
using UnityEngine.UI;

[ExecuteAlways]
public class ImageLerpController : MonoBehaviour
{
    [SerializeField] private ImageLoader imageLoader;

    [Header("Images")]
    [SerializeField] private Texture2D Swap1;
    [SerializeField] private Texture2D Swap2;
    [SerializeField] private Texture2D[] SwapArray;

    [Header("UI / Control")]
    [SerializeField] private Slider imageIndexSlider;
    [SerializeField] private Material globeMaterial; // Material with _LERP property

    [Header("Smoothing Settings")]
    [SerializeField] private float smoothTime = 0.3f;   // How smoothly the slider value transitions
    [SerializeField] private float swapTrigger = 0.98f; // When to prepare next swap (near 1)
    [SerializeField] private float swapRelease = 0.02f; // When to release after wraparound (near 0)

    [Header("Debug / Info")]
    [SerializeField] public string currentImageName; // <-- Stored current image name

    private float targetValue;
    private float smoothedValue;
    private float smoothVelocity;
    private bool usingSwap1 = true;
    private bool hasSwapped = false; // Prevent rapid multiple swaps per transition

    void Start()
    {
        SwapArray = imageLoader.textures;
        if (imageIndexSlider != null)
            imageIndexSlider.onValueChanged.AddListener(OnSliderChanged);

        if (SwapArray != null && SwapArray.Length > 0 && globeMaterial != null)
        {
            Swap1 = SwapArray[0];
            globeMaterial.SetTexture("_Swap1", Swap1);
            currentImageName = Swap1.name;
        }

        smoothedValue = targetValue = imageIndexSlider != null ? imageIndexSlider.value : 0f;
    }

    void Update()
    {
        if (SwapArray == null || SwapArray.Length == 0 || globeMaterial == null) return;

        // Smooth the slider motion
        smoothedValue = Mathf.SmoothDamp(smoothedValue, targetValue, ref smoothVelocity, smoothTime);

        int indexA = Mathf.FloorToInt(smoothedValue);
        int indexB = Mathf.Clamp(indexA + 1, 0, SwapArray.Length - 1);
        float t = smoothedValue - indexA;

        // Assign textures based on active swap state
        if (usingSwap1)
        {
            Swap1 = SwapArray[indexA];
            Swap2 = SwapArray[indexB];
        }
        else
        {
            Swap1 = SwapArray[indexB];
            Swap2 = SwapArray[indexA];
        }

        globeMaterial.SetTexture("_Swap1", Swap1);
        globeMaterial.SetTexture("_Swap2", Swap2);
        globeMaterial.SetFloat("_LERP", usingSwap1 ? t : 1f - t);

        // --- Update the current image name ---
        // Decide which texture is currently dominant (closer to fully visible)
        if (t < 0.5f)
            currentImageName = SwapArray[indexA].name;
        else
            currentImageName = SwapArray[indexB].name;

        // --- Stable swap logic ---
        if (!hasSwapped && t > swapTrigger)
        {
            hasSwapped = true;
            usingSwap1 = !usingSwap1;
        }
        else if (hasSwapped && t < swapRelease)
        {
            hasSwapped = false;
        }
    }

    void OnSliderChanged(float value)
    {
        targetValue = Mathf.Clamp(value, 0, SwapArray.Length - 1);
    }
}
