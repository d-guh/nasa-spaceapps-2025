//
//  UnityTest.swift
//  SpaceApps
//
//  Created by Julia Holzbach on 10/4/25.
//
/*
//import Foundation
import SwiftUI

struct HostingWindowFinder: UIViewRepresentable {
    var callback: (UIWindow?) -> ()
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        DispatchQueue.main.async { [weak view] in
            self.callback(view?.window)
        }
        return view
    }
    
    func updateUIVIew(_uiView: UIView, context: Context) {
    }
}

struct UnityTest: View {
    var body: some View {
        VStack {
            Button(action: {
                Unity.shared.show()
            }, label: {
                Text("Start Game")
            })
        }.background(
            HostingWindowFinder { window in
                Unity.shared.setHostMainWindow(window)
            }
        )
    }
}
*/
    
    
/*struct UnityTest_Previews: PreviewProvider {
    static var previews: some View {
        UnityTest()
    }
}*/

