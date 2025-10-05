using UnityEngine;

public class GlobeDarkness : MonoBehaviour
{
    [SerializeField] private Material globeMaterial;
    [SerializeField] private UIManager uiManager;
    [SerializeField] private Texture2D Swap1;
    [SerializeField] private Texture2D Swap2;
    [SerializeField] private Texture2D[] SwapArray;
    private float opacity = 0;
    private float colored = 0;
    private float velocity = 0;
    private float velocityColor = 0;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (uiManager.OpacityValue)
        {
            opacity = Mathf.SmoothDamp(opacity, 1, ref velocity, 0.5f);
            colored = Mathf.SmoothDamp(colored, 0, ref velocityColor, 0.5f);
        }
        else
        {
            opacity = Mathf.SmoothDamp(opacity, 0, ref velocity, 0.5f);
            colored = Mathf.SmoothDamp(colored, 1, ref velocityColor, 0.5f);
        }


        globeMaterial.SetFloat("_Opacity", opacity);
        globeMaterial.SetFloat("_Colored", colored);
    }
}
