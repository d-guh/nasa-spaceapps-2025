using UnityEngine;

public class ButtonToggle : MonoBehaviour
{
    public bool Toggle;
    [SerializeField] private Animator animator;
    public void ButtonToggleFun()
    {
        Toggle = !Toggle;
        animator.SetBool("Toggle", Toggle);
    }
}